# NoSQL Databases { #nosql-databases }

**FastAPI** doesn't require you to use a SQL (relational) database.

Here we'll see an example using <a href="https://cassandra.apache.org/" class="external-link" target="_blank">Apache Cassandra</a>, a popular distributed NoSQL database.

We'll also show how <a href="https://www.scylladb.com/" class="external-link" target="_blank">ScyllaDB</a>, a Cassandra-compatible database, works using the exact same code.

/// tip

FastAPI doesn't force you to use any specific database. This tutorial demonstrates Cassandra/ScyllaDB, but you can use other databases with their respective Python drivers.

///

## Install Dependencies { #install-dependencies }

First, make sure you create your [virtual environment](../virtual-environments.md){.internal-link target=_blank}, activate it, and then install the Cassandra driver:

<div class="termy">

```console
$ pip install cassandra-driver
---> 100%
```

</div>

/// note

The same `cassandra-driver` works with both Apache Cassandra and ScyllaDB. This is what makes ScyllaDB a true drop-in replacement.

///

/// tip | Python 3.12+

If you're using Python 3.12 or newer, you'll also need an event loop implementation. Install `gevent` for best compatibility:

<div class="termy">

```console
$ pip install gevent
---> 100%
```

</div>

The `asyncore` module was removed in Python 3.12, so `cassandra-driver` requires an alternative event loop like gevent or libev.

///

## Set Up Docker Containers { #set-up-docker-containers }

For local development and testing, you can use Docker Compose to run both Cassandra and ScyllaDB.

Create a `docker-compose.yml` file:

```yaml
services:
  cassandra:
    image: cassandra:4.1
    container_name: fastapi-cassandra
    ports:
      - "9043:9042"
    environment:
      - CASSANDRA_CLUSTER_NAME=test-cluster
    healthcheck:
      test: ["CMD-SHELL", "cqlsh -e 'DESCRIBE KEYSPACES'"]
      interval: 10s
      timeout: 5s
      retries: 10
    volumes:
      - cassandra_data:/var/lib/cassandra

  scylladb:
    image: scylladb/scylla:2025.1.4
    container_name: fastapi-scylladb
    command: --reactor-backend epoll --smp 1 --memory 1G --overprovisioned 1 --api-address 0.0.0.0
    ports:
      - "9042:9042"
    healthcheck:
      test: ["CMD-SHELL", "cqlsh -e 'DESCRIBE KEYSPACES'"]
      interval: 10s
      timeout: 5s
      retries: 10
    volumes:
      - scylladb_data:/var/lib/scylla

volumes:
  cassandra_data:
  scylladb_data:
```

Start the containers:

<div class="termy">

```console
$ docker-compose up -d
```

</div>

/// tip

Notice that both containers expose port 9042 (the CQL native protocol port). We map them to different host ports (9042 and 9043) so both can run simultaneously for comparison.

///

## Create the App { #create-the-app }

We'll create a task management API that demonstrates CRUD operations with Cassandra.

### Import and Create Models { #import-and-create-models }

We use **Pydantic models** for data validation, just like with SQL databases:

{* ../../docs_src/nosql_databases/tutorial001.py ln[1:17] hl[1:5,8:17] *}

/// tip

Unlike SQL databases, Cassandra uses UUIDs for primary keys. This works great in distributed systems because UUIDs can be generated independently on any node without conflicts.

///

### Create the Database Connection { #create-the-database-connection }

Create a connection class that manages the Cassandra cluster, session, and schema:

{* ../../docs_src/nosql_databases/tutorial001.py ln[20:59] hl[20:22,24:26,28:35,37:51] *}

Notice:

* **Cluster** connects to Cassandra nodes (line 21)
* **Session** executes CQL queries (line 25)
* **Keyspace** is like a database/schema in SQL (line 26)
* **Replication** strategy determines how data is distributed

/// note

`SimpleStrategy` with `replication_factor: 1` is for development. In production, use `NetworkTopologyStrategy` with multiple replicas across data centers.

///

### Initialize the Database { #initialize-the-database }

Set up the application and database connection using the modern `lifespan` context manager:

{* ../../docs_src/nosql_databases/tutorial001.py ln[65:81] hl[65,68:74,77] *}

/// tip

We use the `lifespan` context manager to handle startup and shutdown events. This is the recommended approach in modern FastAPI applications. See the <a href="https://fastapi.tiangolo.com/advanced/events/" class="internal-link" target="_blank">events documentation</a> for more details.

///

### Create a Task { #create-a-task }

Add a **POST** endpoint to create tasks:

{* ../../docs_src/nosql_databases/tutorial001.py ln[84:93] hl[84,85,86:92] *}

Key points:

* Generate UUID for primary key
* Use CQL parameterized queries (secure against injection)
* Use `toTimestamp(now())` for Cassandra timestamps

### Read Tasks { #read-tasks }

Add a **GET** endpoint to list all tasks:

{* ../../docs_src/nosql_databases/tutorial001.py ln[96:104] hl[96,97,98:99,100:103] *}

### Read One Task { #read-one-task }

Add a **GET** endpoint for a specific task:

{* ../../docs_src/nosql_databases/tutorial001.py ln[107:112] hl[107,108,109:110,111] *}

### Update a Task { #update-a-task }

Add a **PUT** endpoint to update tasks:

{* ../../docs_src/nosql_databases/tutorial001.py ln[115:131] hl[115,116,117:121,123:127] *}

### Delete a Task { #delete-a-task }

Add a **DELETE** endpoint:

{* ../../docs_src/nosql_databases/tutorial001.py ln[134:144] hl[134,135,136:140,142:143] *}

## Run the App { #run-the-app }

Save the code to `main.py` and run it:

<div class="termy">

```console
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                 │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs              │
 │                                                     │
 │  Running in development mode, for production use:  │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

## Check the API Docs { #check-the-api-docs }

Open your browser at <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

You will see the automatic interactive API documentation (provided by Swagger UI):

<img src="/img/tutorial/nosql-databases/image01.png">

## Use ScyllaDB Instead { #use-scylladb-instead }

**ScyllaDB is Cassandra-compatible**, so you can use it with the same code.

To use ScyllaDB instead of Cassandra, change the **hostname** in the connection:

```python
# Cassandra version (tutorial001.py)
class CassandraConnection:
    def __init__(self, hosts=["cassandra"], port=9042):
        # ... rest of the code stays the same
```

Change to:

```python
# ScyllaDB version (tutorial001_scylla.py)
class ScyllaDBConnection:
    def __init__(self, hosts=["scylladb"], port=9042):
        # ... rest of the code stays the same
```

That's it! Everything else is **identical**:

* ✅ Same Cassandra driver (`cassandra-driver`)
* ✅ Same CQL queries
* ✅ Same data models
* ✅ Same API endpoints
* ✅ Same behavior

The complete ScyllaDB version is in `docs_src/nosql_databases/tutorial001_scylla.py` - the only difference is the hostname.

## Production Considerations { #production-considerations }

### Connection Pooling { #connection-pooling }

The Cassandra driver automatically manages connection pools. For production, configure:

```python
from cassandra.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.policies import DCAwareRoundRobinPolicy, TokenAwarePolicy

profile = ExecutionProfile(
    load_balancing_policy=TokenAwarePolicy(DCAwareRoundRobinPolicy()),
    request_timeout=15
)

cluster = Cluster(
    hosts=['node1', 'node2', 'node3'],
    execution_profiles={EXEC_PROFILE_DEFAULT: profile}
)
```

### Consistency Levels { #consistency-levels }

Cassandra allows tuning consistency per query:

```python
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel

query = SimpleStatement(
    "SELECT * FROM tasks WHERE id = %s",
    consistency_level=ConsistencyLevel.QUORUM
)
session.execute(query, (task_id,))
```

### Error Handling { #error-handling }

Add proper error handling for production:

```python
from cassandra.cluster import NoHostAvailable
from cassandra import OperationTimedOut

try:
    session.execute(query)
except NoHostAvailable:
    raise HTTPException(status_code=503, detail="Database unavailable")
except OperationTimedOut:
    raise HTTPException(status_code=504, detail="Query timeout")
```

### Schema Migrations { #schema-migrations }

For production, use migration tools:

* <a href="https://github.com/Cobliteam/cassandra-migrate" class="external-link" target="_blank">cassandra-migrate</a>
* Custom CQL scripts with version tracking
* Application-level schema management

## Learn More { #learn-more }

This is a quick introduction. For more advanced topics, see:

* <a href="https://cassandra.apache.org/doc/latest/" class="external-link" target="_blank">Cassandra Documentation</a>
* <a href="https://opensource.docs.scylladb.com/" class="external-link" target="_blank">ScyllaDB Documentation</a>
* <a href="https://docs.datastax.com/en/developer/python-driver/" class="external-link" target="_blank">DataStax Python Driver Documentation</a>

## Recap { #recap }

FastAPI works great with NoSQL databases like Cassandra and ScyllaDB:

* ✅ Use standard Python drivers
* ✅ Leverage Pydantic for data validation
* ✅ Get automatic API documentation
* ✅ Enjoy type safety and editor support
* ✅ Switch between compatible databases with minimal changes

FastAPI works well with NoSQL databases, providing the same benefits as with SQL databases.
