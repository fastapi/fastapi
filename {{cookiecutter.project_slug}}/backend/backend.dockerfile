FROM python:3.6

RUN pip install celery==4.2.1 passlib[bcrypt] tenacity requests pydantic emails fastapi>=0.2.0 uvicorn gunicorn pyjwt python-multipart email_validator jinja2 psycopg2-binary alembic SQLAlchemy

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter notebook --ip=0.0.0.0 --allow-root
ARG env=prod
RUN bash -c "if [ $env == 'dev' ] ; then pip install jupyter ; fi"
EXPOSE 8888

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 80

CMD ["bash", "/app/backend-start.sh"]
