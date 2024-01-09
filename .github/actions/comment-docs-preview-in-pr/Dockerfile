FROM python:3.10

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./app /app

CMD ["python", "/app/main.py"]
