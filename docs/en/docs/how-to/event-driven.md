# Event-driven services

**FastAPI** supports HTTP protocol only, so you should use broker clients to implement event-driven logic:

* <a href="https://docs.aio-pika.com/" class="external-link" target="_blank">aio-pika</a> for **RabbitMQ**
* <a href="https://aiokafka.readthedocs.io/" class="external-link" target="_blank">aiokafka</a> for **Kafka**
* <a href="https://nats-io.github.io/nats.py/" class="external-link" target="_blank">nats-py</a> for **NATS**

But if you would like to get the same experience in
event-driven services development, you should take a look at <a href="https://faststream.airt.ai/latest/" class="external-link" target="_blank">**FastStream** framework</a>.

This tool is strongly inspired by **FastAPI** and has a pretty close design - it's based on type annotations
to serialize incoming messages, decorators to register consumers, and generate your application specification from the code automatically.

Also, **FastStream** has a special integration with **FastAPI**, so you can declare event consumers and HTTP endpoints
on the same **FastAPI** application.

## FastStream integration

For now, **FastStream** supports **Kafka**, **RabbitMQ**, **Nats**, and **Redis** brokers as a backend.
So you can easily integrate such brokers into your **FastAPI** application.

Here's a small preview of each broker's usage:

/// tab | Kafka
{* ../../docs_src/event_driven/faststream_kafka.py hl[3,6,14,15,16,20] *}
///

/// tab | RabbitMQ
{* ../../docs_src/event_driven/faststream_rabbit.py hl[3,6,14,15,16,20] *}
///

/// tab | NATS
{* ../../docs_src/event_driven/faststream_nats.py hl[3,6,14,15,16,20] *}
///

/// tab | Redis
{* ../../docs_src/event_driven/faststream_redis.py hl[3,6,14,15,16,20] *}
///

/// tip

This integration supports **fastapi.Depends**, **BackgroundTasks**, **Headers**, **Query**, and most of **FastAPI** features you are familiar with.

///

You can learn more about **FastStream** in the <a href="https://faststream.airt.ai/latest/" class="external-link" target="_blank">**FastStream** documentation</a>.

And also the docs about <a href="https://faststream.airt.ai/latest/getting-started/integrations/fastapi/" class="external-link" target="_blank">**FastStream** with **FastAPI**</a>.

### AsyncAPI Specification

**FastStream** also generates [**AsyncAPI** specification](https://www.asyncapi.com/en){.external-link} for your event-driven services from the code the same way with **FastAPI** generates **OpenAPI** for your HTTP endpoints. So
You can see your event-driven endpoints right in the web representation the same way you can with the **Swagger UI** way.

<img src="/img/tutorial/event-driven/AsyncAPI-basic-html-full.png">
