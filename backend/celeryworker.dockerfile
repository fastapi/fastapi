FROM python:3.10

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

ENV C_FORCE_ROOT=1

ENV PYTHONPATH=/app

COPY ./alembic.ini /app/

COPY ./worker-start.sh /worker-start.sh

COPY ./app /app/app

RUN chmod +x /worker-start.sh

CMD ["bash", "/worker-start.sh"]
