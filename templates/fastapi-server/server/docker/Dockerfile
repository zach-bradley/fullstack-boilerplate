# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file from the root directory (build context)
COPY requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# The command will be provided by docker-compose.yml
