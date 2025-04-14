from flask import Flask, request, redirect, jsonify, send_from_directory
import string
import random
import redis
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

# Redis configuration
redis_host = os.getenv("REDIS_HOST", "redis")  # Use 'redis' as the default hostname
redis_port = int(os.getenv("REDIS_PORT", "6379"))

try:
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
    redis_client.ping()  # Test connection
except redis.ConnectionError as e:
    app.logger.error(f"Redis connection error: {e}")
    raise RuntimeError("Failed to connect to Redis. Ensure Redis is running and accessible.")

def generate_short_id(num_chars=6):
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url')
    if not long_url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        existing_short_id = redis_client.get(long_url)
        if existing_short_id:
            return jsonify({'short_url': request.host_url + existing_short_id}), 201

        short_id = generate_short_id()
        redis_client.set(long_url, short_id)
        redis_client.set(short_id, long_url)

        short_url = request.host_url + short_id
        return jsonify({'short_url': short_url}), 201
    except redis.ConnectionError as e:
        app.logger.error(f"Redis connection error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/<short_id>')
def redirect_url(short_id):
    try:
        long_url = redis_client.get(short_id)
        if long_url:
            return redirect(long_url)
        return jsonify({'error': 'Invalid URL'}), 404
    except redis.ConnectionError as e:
        app.logger.error(f"Redis connection error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
