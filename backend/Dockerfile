# Use a lightweight Python image for faster startup
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install pip dependencies first for better layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose the Flask port
EXPOSE 5000

# Default command runs the Flask app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
