from flask import Flask, request, redirect, jsonify
import string
import random

app = Flask(__name__)

# In-memory dictionary to store URL mappings
url_mapping = {}

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
    url_mapping[short_id] = long_url
    short_url = request.host_url + short_id
    return jsonify({'short_url': short_url}), 201

@app.route('/<short_id>')
def redirect_url(short_id):
    long_url = url_mapping.get(short_id)
    if long_url:
        return redirect(long_url)
    return jsonify({'error': 'Invalid URL'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

