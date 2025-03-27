FROM python:3.12.3

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY server.py .

# Expose the application port
EXPOSE 5000

CMD ["python", "server.py"]
