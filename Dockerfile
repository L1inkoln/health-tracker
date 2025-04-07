FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Bсполняемый скрипт при запуске
CMD ["bash", "-c", "uvicorn app.main:app & sleep 2 && python bot/main.py"]
