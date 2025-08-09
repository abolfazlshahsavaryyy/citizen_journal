# ----------------------------
# 1. Use a lightweight base image
# ----------------------------
FROM python:3.12-slim AS base

# Prevent Python from writing pyc files & buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ----------------------------
# 2. Install system dependencies (only what's needed)
# ----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libhdf5-dev \
    libgl1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# 3. Set working directory
# ----------------------------
WORKDIR /app

# ----------------------------
# 4. Copy requirements first (better layer caching)
# ----------------------------
COPY requirements.txt .

# Upgrade pip & install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ----------------------------
# 5. Copy application code (including models)
# ----------------------------
COPY . .

# ----------------------------
# 6. Create non-root user and fix permissions
# ----------------------------
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

# ----------------------------
# 7. Expose port & run FastAPI
# ----------------------------
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
