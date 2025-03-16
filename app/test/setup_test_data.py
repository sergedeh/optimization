import requests

BASE_URL = "http://127.0.0.1:8000"

def create_user(email, password):
    response = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    print("User Created:", response.json())

def login_user(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    token = response.json().get("access_token")
    print("User Logged In:", response.json())
    return token

def create_plan(name, price, duration_days):
    response = requests.post(f"{BASE_URL}/plans/plans", json={"name": name, "price": price, "duration_days": duration_days})
    print("Plan Created:", response.json())

def subscribe_user(user_id, plan_id):
    response = requests.post(f"{BASE_URL}/subscriptions/subscribe", json={"user_id": user_id, "plan_id": plan_id})
    print("User Subscribed:", response.json())

if __name__ == "__main__":
    # Setup Test Data
    create_user("testuser5@example.com", "password123")
    token = login_user("testuser5@example.com", "password123")

    # Create Subscription Plans
    create_plan("Basic", 10, 30)
    create_plan("Pro", 20, 60)
    create_plan("Premium", 50, 365)

    # # Subscribe User to a Plan
    subscribe_user(1, 1)
    subscribe_user(1, 2)
