FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY download_data.py .
COPY start.sh .

# Make start script executable
RUN chmod +x start.sh

# Create data directory
RUN mkdir -p /app/data/csv

# Expose port
EXPOSE 8000

CMD ["./start.sh"]
