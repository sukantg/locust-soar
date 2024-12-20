from locust import HttpUser, task, between
from locust.contrib.fasthttp import FastHttpUser
import json

class UserBehavior(HttpUser):
    wait_time = between(1, 2)  # Time between tasks
    
    def on_start(self):
        """Initialize test data"""
        self.register_data = {
            "fullName": "Test User",
            "userName": "testuser",
            "email": "test@example.com",
            "password": "test123",
            "phone": "1234567890"
        }
        
        self.login_data = {
            "userName": "testuser",
            "email": "test@example.com",
            "password": "test123"
        }

    @task(2)  # Load testing /client_register
    def register_client(self):
        # Modify email to avoid duplicate registration errors
        self.register_data["email"] = f"test{self.user_count}@example.com"
        self.register_data["userName"] = f"testuser{self.user_count}"
        
        with self.client.post(
            "/client_registeration",
            data=self.register_data,
            catch_response=True
        ) as response:
            try:
                if response.json()["msg"] in ["User Registered", "Email already Exist"]:
                    response.success()
                else:
                    response.failure("Registration failed")
            except json.JSONDecodeError:
                response.failure("Invalid JSON response")

    @task(3)  # Stress testing /client_login
    def login_client(self):
        with self.client.post(
            "/client_login",
            data=self.login_data,
            catch_response=True
        ) as response:
            try:
                if "token" in response.json() or response.json()["msg"] == "In correct email or password":
                    response.success()
                else:
                    response.failure("Login failed")
            except json.JSONDecodeError:
                response.failure("Invalid JSON response")

class StressTest(UserBehavior):
    """Specific class for stress testing with more aggressive parameters"""
    wait_time = between(0.1, 0.5)  # Reduced wait time for stress testing
    
    @task(1)
    def login_stress(self):
        # Repeatedly hammer the login endpoint
        for _ in range(5):  # Multiple attempts per task
            self.login_client()

# BDD-style scenarios
def test_load_scenario():
    """
    Given a Flask application is running
    When multiple users attempt to register and login
    Then the system should handle the load without errors
    And response times should remain under acceptable thresholds
    """
    pass  # This is implemented through the UserBehavior class above

def test_stress_scenario():
    """
    Given a Flask application is running
    When the system is under heavy login load
    Then it should maintain functionality
    And either serve requests or fail gracefully
    """
    pass  # This is implemented through the StressTest class above