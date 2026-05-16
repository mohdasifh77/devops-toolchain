import sqlite3
from datetime import datetime
from typing import Optional

# Single shared in-memory connection used by both app and tests
_conn = sqlite3.connect(':memory:', check_same_thread=False)
_conn.row_factory = sqlite3.Row

def _setup(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            description TEXT    DEFAULT '',
            status      TEXT    DEFAULT 'pending',
            priority    TEXT    DEFAULT 'medium',
            created_at  TEXT    NOT NULL,
            updated_at  TEXT    NOT NULL
        )
    ''')
    conn.commit()

_setup(_conn)

class Database:
    def __init__(self, conn=None):
        self.conn = conn or _conn

    def use_new_connection(self, path=':memory:'):
        """Replace connection — used by tests for isolation."""
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        _setup(self.conn)

    def init(self):
        _setup(self.conn)
        count = self.conn.execute('SELECT COUNT(*) FROM tasks').fetchone()[0]
        if count == 0:
            now = datetime.utcnow().isoformat()
            for title, desc, status, priority in [
                ('Set up Jenkins pipeline',  'Configure CI/CD',      'done',    'high'),
                ('Configure SonarQube',      'Code quality gates',   'done',    'high'),
                ('Set up Nexus registry',    'Artifact storage',     'pending', 'high'),
                ('Write unit tests',         'Achieve 80% coverage', 'pending', 'medium'),
                ('Configure Nginx proxy',    'Reverse proxy setup',  'pending', 'medium'),
                ('Add Docker security scan', 'Trivy integration',    'pending', 'low'),
            ]:
                self.conn.execute(
                    'INSERT INTO tasks (title,description,status,priority,created_at,updated_at) VALUES (?,?,?,?,?,?)',
                    (title, desc, status, priority, now, now)
                )
            self.conn.commit()

    def is_connected(self) -> bool:
        try:
            self.conn.execute('SELECT 1')
            return True
        except Exception:
            return False

    def get_tasks(self, status=None, priority=None):
        q, p = 'SELECT * FROM tasks WHERE 1=1', []
        if status:   q += ' AND status=?';   p.append(status)
        if priority: q += ' AND priority=?'; p.append(priority)
        q += ' ORDER BY created_at DESC'
        return [dict(r) for r in self.conn.execute(q, p).fetchall()]

    def get_task(self, task_id: int) -> Optional[dict]:
        row = self.conn.execute('SELECT * FROM tasks WHERE id=?', (task_id,)).fetchone()
        return dict(row) if row else None

    def create_task(self, title: str, description: str = '', priority: str = 'medium') -> dict:
        now = datetime.utcnow().isoformat()
        cur = self.conn.execute(
            'INSERT INTO tasks (title,description,status,priority,created_at,updated_at) VALUES (?,?,?,?,?,?)',
            (title, description, 'pending', priority, now, now)
        )
        self.conn.commit()
        return self.get_task(cur.lastrowid)

    def update_task(self, task_id: int, data: dict) -> dict:
        updates = {k: v for k, v in data.items() if k in {'title','description','status','priority'}}
        if not updates:
            return self.get_task(task_id)
        updates['updated_at'] = datetime.utcnow().isoformat()
        clause = ', '.join(f'{k}=?' for k in updates)
        self.conn.execute(f'UPDATE tasks SET {clause} WHERE id=?', list(updates.values()) + [task_id])
        self.conn.commit()
        return self.get_task(task_id)

    def delete_task(self, task_id: int):
        self.conn.execute('DELETE FROM tasks WHERE id=?', (task_id,))
        self.conn.commit()

    def get_stats(self) -> dict:
        c = self.conn
        return {
            'total':         c.execute('SELECT COUNT(*) FROM tasks').fetchone()[0],
            'pending':       c.execute("SELECT COUNT(*) FROM tasks WHERE status='pending'").fetchone()[0],
            'done':          c.execute("SELECT COUNT(*) FROM tasks WHERE status='done'").fetchone()[0],
            'high_priority': c.execute("SELECT COUNT(*) FROM tasks WHERE priority='high'").fetchone()[0],
        }
