# Containerized URL Shortener Application

## Week 1

### Run both redis and url shortener
```
docker-compose up --build
```

### Test the service
```
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.google.com"}' http://localhost:5000/shorten
```
You should receive a JSON response with a generated short URL. Navigating to that short URL should redirect you to the original long URL.

### Stop the running containers
```
docker-compose down
```

## Week 2

### Start a Minikube Kubernetes cluster using Docker as the driver
``` 
minikube start --driver=docker 
```

### Load the url-shortener:latest image into the Minikube cluster
```
minikube image load url-shortener:latest
```

### Deployments
``` 
kubectl apply -f redis-deployment.yaml
kubectl apply -f url-shortener-deployment.yaml
```

### Services
``` 
kubectl apply -f redis-service.yaml 
kubectl apply -f url-shortener-service.yaml
```

### Config Map
```
kubectl apply -f configmap.yaml
```

### Retrieve the URL for accessing the url-shortener-service externally
```
minikube service url-shortener-service --url
```

### Test the service on a new terminal
```
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.google.com"}' http://EXTERNAL_URL/shorten
```
You should receive a JSON response with a generated short URL. Navigating to that short URL should redirect you to the original long URL.

## Week 3

### Install metrics-serve Addon on minikube
```
minikube addons enable metrics-server
```

### Verify the installation of metrics-server
```
kubectl get deployment metrics-server -n kube-system
```

### Apply the cpu-hpa.yaml config to the deployment
```
kubectl apply -f .\url-shortener-service.yaml
```

### Check the usage of the CPU
```
kubectl get hpa
```

### Check the number of replications
```
kubectl get top pods
```
### Install and Run locust on terminal 
```
pip3 install locust
locust
```
### Follow the url for the Locust Web UI
```
http://localhost:8089/
```
### Add the Deployment url in the Host section on Locust 
```
http://127.0.0.1:54756/  #the port number may change
```

### Change the number of concurrent users
```
example : Number of users (peak concurrency)
          100000

          Ramp up (users started/seconds)
          1000
```
### Again check the usage of the CPU
```
kubectl get hpa
```
### Again check the number of replications of the containers (must have increased)
```
kubectl get top pods
```