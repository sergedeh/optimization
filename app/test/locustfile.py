from locust import HttpUser, task, between, events
import subprocess
import os

subprocess.run(["python", "app/test/reset_db.py"], check=True)
subprocess.run(["python", "app/test/setup_test_data.py"], check=True)

class SubscriptionTest(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def subscribe_user(self):
        self.client.post("/subscriptions/subscribe", json={"user_id": 1, "plan_id": 2})

    @task(1)
    def cancel_subscription(self):
        self.client.post("/subscriptions/subscriptions/5/cancel")

    @task(1)
    def list_active_subscriptions(self):
        self.client.get("/subscriptions/subscriptions/5/active")

@events.quitting.add_listener
def cleanup(environment, **kwargs):
    print("Cleaning up test data after performance testing...")
    subprocess.run(["python", "app/test/reset_db.py"], check=True)