FROM python:3.13-slim

WORKDIR /app

# Create the logs directory explicitly
RUN mkdir -p /logs && chmod 777 /logs

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]