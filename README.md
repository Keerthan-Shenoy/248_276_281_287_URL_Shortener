# Containerized URL Shortener

## Commands

### Build the docker image
docker build -t url-shortener .

### Run the container
docker run -d -p 5000:5000 url-shortener

### Test the service
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.google.com"}' http://localhost:5000/shorten
You should receive a JSON response with a generated short URL. Navigating to that short URL should redirect you to the original long URL.
