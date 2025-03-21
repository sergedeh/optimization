from locust import HttpUser, task, between, events
import subprocess
import os
import random

subprocess.run(["python", "app/test/reset_db.py"], check=True)
subprocess.run(["python", "app/test/setup_test_data.py"], check=True)

class SubscriptionTest(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def subscribe_user(self):
        user_id = random.randint(1, 1000)
        plan_id = random.choice([1, 2, 3])
        self.client.post("/subscriptions/subscribe", json={"user_id": user_id, "plan_id": plan_id})

    @task(2)
    def cancel_subscription(self):
        user_id = random.randint(1, 1000)
        self.client.post(f"/subscriptions/subscriptions/{user_id}/cancel")

    @task(3)
    def list_active_subscriptions(self):
        user_id = random.randint(1, 1000)
        self.client.get(f"/subscriptions/subscriptions/{user_id}/active")

@events.quitting.add_listener
def cleanup(environment, **kwargs):
    print("Cleaning up test data after performance testing...")
    subprocess.run(["python", "app/test/reset_db.py"], check=True)