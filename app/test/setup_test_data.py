import requests
import random

BASE_URL = "http://127.0.0.1:8000"

def create_user(user_id, role="user"):
    """Register a user with a specific role."""
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/auth/register",
                             json={"email": f"user{user_id}@gmail.com", "password": "password", "role": role},
                             headers=headers)
    print("User Created:", response.json())

def login_user(email, password):
    """Login user and retrieve JWT token"""
    response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    token = response.json().get("access_token")
    print("User Logged In:", response.json())
    return token

def create_plan(name, price, duration_days, admin_token):
    """Admin creates a plan"""
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {admin_token}"}
    response = requests.post(f"{BASE_URL}/plans/plans",
                             json={"name": name, "price": price, "duration_days": duration_days},
                             headers=headers)

    print("Plan Created:", response.json())

def subscribe_user(user_id, plan_id, user_token):
    """User subscribes to a plan"""
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {user_token}"}
    response = requests.post(f"{BASE_URL}/subscriptions/subscribe",
                             json={"user_id": user_id, "plan_id": plan_id},
                             headers=headers)
    print("User Subscribed:", response.json())

if __name__ == "__main__":
    # Create an admin user and get an admin token
    create_user("admin", role="admin")
    admin_token = login_user("useradmin@gmail.com", "password")

    # Create plans using admin privileges
    create_plan("Basic", 10, 30, admin_token)
    create_plan("Pro", 20, 60, admin_token)
    create_plan("Premium", 50, 365, admin_token)

    # Create 100 users and subscribe them to random plans
    for user_id in range(1, 101):
        create_user(user_id, role="user")
        user_token = login_user(f"user{user_id}@gmail.com", "password")
        plan_id = random.choice([1, 2, 3]) 
        subscribe_user(user_id, plan_id, user_token) 
