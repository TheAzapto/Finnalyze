# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system deps if needed later (for yfinance / SSL / etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code (app.py + others)
COPY . .

# Flask runs on port 5000
EXPOSE 5000

CMD ["python", "app.py"]
