FROM python:3.12-slim

# Install system deps
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first
COPY fast_api/requirements.txt .

RUN pip --default-timeout=100 install --no-cache-dir -r requirements.txt
# Copy app code
COPY fast_api .

# Expose port (inside container)
EXPOSE 8003

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]




