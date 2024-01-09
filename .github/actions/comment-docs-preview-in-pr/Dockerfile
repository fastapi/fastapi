FROM python:3.9

RUN pip install httpx "pydantic==1.5.1" pygithub

COPY ./app /app

CMD ["python", "/app/main.py"]
