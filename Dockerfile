FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY main.py .
COPY test_main.py .

RUN pip install fastapi uvicorn pydantic sqlalchemy psycopg2-binary pytest httpx

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]