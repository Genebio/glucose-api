FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a directory for the database with proper permissions
RUN mkdir -p /data && chmod 777 /data
ENV DATABASE_URL=sqlite:////data/glucose.db

# Run as non-root for security
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser:appuser /app /data
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]