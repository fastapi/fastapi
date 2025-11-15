from contextlib import asynccontextmanager
from typing import List, Union
from uuid import UUID, uuid4

from cassandra.cluster import Cluster
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str
    description: Union[str, None] = None
    status: str = "pending"


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: UUID = Field(default_factory=uuid4)


class CassandraConnection:
    def __init__(self, hosts=None, port=9042):
        if hosts is None:
            hosts = ["cassandra"]

        self.cluster = Cluster(hosts, port=port)
        self.session = None
        self.keyspace = "task_manager"

    def connect(self):
        self.session = self.cluster.connect()
        self.create_keyspace()
        self.session.set_keyspace(self.keyspace)
        self.create_table()

    def create_keyspace(self):
        self.session.execute(
            f"""
            CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
            WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
            """
        )

    def create_table(self):
        self.session.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id uuid PRIMARY KEY,
                title text,
                description text,
                status text,
                created_at timestamp,
                updated_at timestamp
            )
            """
        )

    def close(self):
        if self.session:
            self.session.shutdown()
        if self.cluster:
            self.cluster.shutdown()


db = CassandraConnection()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    db.connect()
    yield
    # Shutdown
    db.close()


app = FastAPI(lifespan=lifespan)


def get_db():
    return db.session


@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate, session=Depends(get_db)):
    task_id = uuid4()
    query = """
        INSERT INTO tasks (id, title, description, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, toTimestamp(now()), toTimestamp(now()))
    """
    session.execute(query, (task_id, task.title, task.description, task.status))
    return Task(
        id=task_id, title=task.title, description=task.description, status=task.status
    )


@app.get("/tasks/", response_model=List[Task])
def read_tasks(session=Depends(get_db)):
    query = "SELECT id, title, description, status FROM tasks"
    rows = session.execute(query)
    return [
        Task(id=row.id, title=row.title, description=row.description, status=row.status)
        for row in rows
    ]


@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: UUID, session=Depends(get_db)):
    query = "SELECT id, title, description, status FROM tasks WHERE id = %s"
    row = session.execute(query, (task_id,)).one()
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(
        id=row.id, title=row.title, description=row.description, status=row.status
    )


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task: TaskCreate, session=Depends(get_db)):
    # Check if task exists
    check_query = "SELECT id FROM tasks WHERE id = %s"
    existing = session.execute(check_query, (task_id,)).one()
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")

    update_query = """
        UPDATE tasks
        SET title = %s, description = %s, status = %s, updated_at = toTimestamp(now())
        WHERE id = %s
    """
    session.execute(update_query, (task.title, task.description, task.status, task_id))
    return Task(
        id=task_id, title=task.title, description=task.description, status=task.status
    )


@app.delete("/tasks/{task_id}")
def delete_task(task_id: UUID, session=Depends(get_db)):
    # Check if task exists
    check_query = "SELECT id FROM tasks WHERE id = %s"
    existing = session.execute(check_query, (task_id,)).one()
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")

    delete_query = "DELETE FROM tasks WHERE id = %s"
    session.execute(delete_query, (task_id,))
    return {"ok": True}
