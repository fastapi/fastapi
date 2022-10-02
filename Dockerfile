# Create image from lightweight python3-alpine (https://hub.docker.com/_/python).
FROM python:3-alpine

# Exposes container port 8000.
EXPOSE 8000/tcp

# Set working directory.
WORKDIR /usr/src/app

# Install git and common text editors.
RUN apk add git
RUN apk add vim
RUN apk add nano

# Clone FastAPI Github repo. (https://github.com/tiangolo/fastapi)
RUN git clone https://github.com/tiangolo/fastapi.git tmp/
RUN mv tmp/tests/ .
RUN rm -r tmp

# Install required FastAPI packages.
RUN pip install --no-cache-dir fastapi
RUN pip install uvicorn[standard]

# Docker run command.
# docker run -it -rm --name FastAPI -p 8000:8000 -w /usr/src/app/tests fastapi:python3-alpine uvicorn --host 0.0.0.0 main:app --reload
