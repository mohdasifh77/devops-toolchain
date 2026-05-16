import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app, db

@pytest.fixture(autouse=True)
def fresh_db():
    # Give each test a brand new in-memory SQLite connection
    db.use_new_connection(':memory:')
    yield

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

class TestHealth:
    def test_health_returns_200(self, client):
        assert client.get('/health').status_code == 200

    def test_health_contains_status(self, client):
        data = client.get('/health').get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'devops-toolchain-app'

    def test_ready_returns_200(self, client):
        assert client.get('/ready').get_json()['ready'] is True

    def test_metrics_returns_counts(self, client):
        data = client.get('/metrics').get_json()
        assert 'total_tasks' in data
        assert 'pending_tasks' in data

class TestTaskCRUD:
    def test_list_tasks_returns_200(self, client):
        res = client.get('/api/tasks')
        assert res.status_code == 200
        assert 'tasks' in res.get_json()

    def test_create_task_success(self, client):
        res = client.post('/api/tasks', json={'title': 'Test Task', 'priority': 'high'})
        assert res.status_code == 201
        data = res.get_json()
        assert data['title'] == 'Test Task'
        assert data['priority'] == 'high'
        assert data['status'] == 'pending'

    def test_create_task_missing_title(self, client):
        assert client.post('/api/tasks', json={}).status_code == 400

    def test_create_task_invalid_priority(self, client):
        assert client.post('/api/tasks', json={'title': 'T', 'priority': 'urgent'}).status_code == 400

    def test_get_task_by_id(self, client):
        created = client.post('/api/tasks', json={'title': 'Find Me'}).get_json()
        res = client.get(f'/api/tasks/{created["id"]}')
        assert res.status_code == 200
        assert res.get_json()['title'] == 'Find Me'

    def test_get_task_not_found(self, client):
        assert client.get('/api/tasks/99999').status_code == 404

    def test_update_task(self, client):
        created = client.post('/api/tasks', json={'title': 'Old'}).get_json()
        res = client.put(f'/api/tasks/{created["id"]}', json={'title': 'New'})
        assert res.status_code == 200
        assert res.get_json()['title'] == 'New'

    def test_complete_task(self, client):
        created = client.post('/api/tasks', json={'title': 'Do Me'}).get_json()
        res = client.patch(f'/api/tasks/{created["id"]}/complete')
        assert res.status_code == 200
        assert res.get_json()['status'] == 'done'

    def test_delete_task(self, client):
        created = client.post('/api/tasks', json={'title': 'Kill Me'}).get_json()
        assert client.delete(f'/api/tasks/{created["id"]}').status_code == 200
        assert client.get(f'/api/tasks/{created["id"]}').status_code == 404

    def test_filter_by_status(self, client):
        client.post('/api/tasks', json={'title': 'P'})
        tasks = client.get('/api/tasks?status=pending').get_json()['tasks']
        assert all(t['status'] == 'pending' for t in tasks)

    def test_filter_by_priority(self, client):
        client.post('/api/tasks', json={'title': 'H', 'priority': 'high'})
        tasks = client.get('/api/tasks?priority=high').get_json()['tasks']
        assert all(t['priority'] == 'high' for t in tasks)
