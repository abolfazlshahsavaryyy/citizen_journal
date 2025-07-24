# Dockerfile

FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first (optimize cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole fastapi_app folder content into /app
COPY . .

# Expose port 8001
EXPOSE 8001
ENV PYTHONPATH=/app
# Run the app with uvicorn on port 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
