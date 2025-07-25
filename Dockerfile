# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Load environment variables from .env
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "securityBot.py"]
