import requests
import random

BASE_URL = "http://127.0.0.1:8000"

def create_user(user_id):
    response = requests.post(f"{BASE_URL}/auth/register", json={"email": f"user{user_id}@gmail.com", "password": "password"})
    print("User Created:", response.json())

def login_user(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    token = response.json().get("access_token")
    print("User Logged In:", response.json())
    return token

def create_plan(name, price, duration_days):
    response = requests.post(f"{BASE_URL}/plans/plans", json={"name": name, "price": price, "duration_days": duration_days})
    print("Plan Created:", response.json())

async def subscribe_user(user_id, plan_id):
    response = await requests.post(f"{BASE_URL}/subscriptions/subscribe", json={"user_id": user_id, "plan_id": plan_id})
    print("User Subscribed:", response.json())

if __name__ == "__main__":
    # Setup Test Data
    # create_user("testuser5@example.com", "password123")
    # token = login_user("testuser5@example.com", "password123")

    # Create Subscription Plans
    create_plan("Basic", 10, 30)
    create_plan("Pro", 20, 60)
    create_plan("Premium", 50, 365)

    # # Subscribe User to a Plan
    for user_id in range(1, 101):
        create_user(user_id)
        plan_id = random.choice([1, 2, 3])  # Randomly pick a plan
        subscribe_user(user_id, plan_id)
