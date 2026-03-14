FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (for Docker cache)
COPY requirements.txt /app/bookbot/requirements.txt
RUN pip install --no-cache-dir -r /app/bookbot/requirements.txt

# Copy application code into the bookbot package directory
COPY . /app/bookbot/

CMD ["python", "/app/bookbot/bot.py"]
