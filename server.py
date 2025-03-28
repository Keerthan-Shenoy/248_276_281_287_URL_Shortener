from flask import Flask, request, redirect, jsonify
import string
import random
import redis
import os

app = Flask(__name__)

# In-memory dictionary to store URL mappings
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)

def generate_short_id(num_chars=6):
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url')
    if not long_url:
        return jsonify({'error': 'URL is required'}), 400
    short_id = generate_short_id()
    redis_client.set(short_id, long_url)
    short_url = request.host_url + short_id
    return jsonify({'short_url': short_url}), 201

@app.route('/<short_id>')
def redirect_url(short_id):
    long_url = redis_client.get(short_id)
    if long_url:
        return redirect(long_url)
    return jsonify({'error': 'Invalid URL'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

