FROM python:3.10-slim

WORKDIR /app/backend

# system deps for psycopg2
RUN apt-get update && apt-get install -y build-essential libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
