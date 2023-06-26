FROM python:3.7

RUN pip install httpx PyGithub "pydantic==1.5.1" "pyyaml>=5.3.1,<6.0.0"

COPY ./app /app

CMD ["python", "/app/main.py"]
