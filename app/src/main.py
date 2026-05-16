from flask import Flask, jsonify, request, abort
from database import Database
from datetime import datetime
import os

app = Flask(__name__)
app.config['VERSION'] = os.getenv('APP_VERSION', '1.0.0')
app.config['ENV']     = os.getenv('FLASK_ENV', 'production')

db = Database()

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 'service': 'devops-toolchain-app',
        'version': app.config['VERSION'], 'env': app.config['ENV'],
        'timestamp': datetime.utcnow().isoformat(),
        'db': 'connected' if db.is_connected() else 'disconnected',
    })

@app.route('/ready')
def ready():
    return jsonify({'ready': True})

@app.route('/metrics')
def metrics():
    s = db.get_stats()
    return jsonify({'total_tasks': s['total'], 'pending_tasks': s['pending'],
                    'done_tasks': s['done'], 'high_priority': s['high_priority']})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = db.get_tasks(status=request.args.get('status'), priority=request.args.get('priority'))
    return jsonify({'tasks': tasks, 'total': len(tasks)})

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = db.get_task(task_id)
    if not task: abort(404, description='Task not found')
    return jsonify(task)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title'): abort(400, description='title is required')
    priority = data.get('priority', 'medium')
    if priority not in ('low', 'medium', 'high'): abort(400, description='priority must be low, medium, or high')
    return jsonify(db.create_task(data['title'], data.get('description', ''), priority)), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if not db.get_task(task_id): abort(404, description='Task not found')
    return jsonify(db.update_task(task_id, request.get_json() or {}))

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if not db.get_task(task_id): abort(404, description='Task not found')
    db.delete_task(task_id)
    return jsonify({'message': 'Task deleted'})

@app.route('/api/tasks/<int:task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    if not db.get_task(task_id): abort(404, description='Task not found')
    return jsonify(db.update_task(task_id, {'status': 'done'}))

@app.errorhandler(400)
def bad_request(e): return jsonify({'error': str(e.description)}), 400

@app.errorhandler(404)
def not_found(e): return jsonify({'error': str(e.description)}), 404

if __name__ == '__main__':
    db.init()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
