FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install -r requirements.txt

# Copy source
COPY . .

# Activate virtualenv
ENV PATH="/opt/venv/bin:$PATH"

# Expose port inside container
EXPOSE 5000

# Gunicorn command is defined by docker-compose
