from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def shorten_url(self):
        self.client.post("/shorten", json={"url": "https://www.google.com"})  
