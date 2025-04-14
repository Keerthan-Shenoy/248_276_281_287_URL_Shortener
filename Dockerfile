FROM python:3.12.3

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code (including index.html and server.py)
COPY . .

# Expose the application port
EXPOSE 5000

# Run the application
CMD ["python", "server.py"]
