from locust import HttpUser, task, between
import json
import random

class UserBehavior(HttpUser):
    wait_time = between(1, 2)  # Time between tasks
    
    def on_start(self):
        """Initialize test data"""
        # Generate unique identifier for this user instance
        self.user_id = random.randint(1000, 9999)
        
        self.register_data = {
            "fullName": f"Test User {self.user_id}",
            "userName": f"testuser{self.user_id}",
            "email": f"test{self.user_id}@example.com",
            "password": "test123",
            "phone": f"123{self.user_id}"
        }
        
        self.login_data = {
            "userName": f"testuser{self.user_id}",
            "email": f"test{self.user_id}@example.com",
            "password": "test123"
        }

    @task(2)  # Load testing /client_register
    def register_client(self):
        with self.client.post(
            "/client_registeration",
            data=self.register_data,
            catch_response=True
        ) as response:
            try:
                if response.json()["msg"] in ["User Registered", "Email already Exist"]:
                    response.success()
                else:
                    response.failure(f"Registration failed: {response.json()}")
            except json.JSONDecodeError:
                response.failure("Invalid JSON response")
            except Exception as e:
                response.failure(f"Error: {str(e)}")

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
                    response.failure(f"Login failed: {response.json()}")
            except json.JSONDecodeError:
                response.failure("Invalid JSON response")
            except Exception as e:
                response.failure(f"Error: {str(e)}")

class StressTest(UserBehavior):
    """Specific class for stress testing with more aggressive parameters"""
    wait_time = between(0.1, 0.5)  # Reduced wait time for stress testing
    
    @task(1)
    def login_stress(self):
        # Create random login attempts
        random_user_id = random.randint(1000, 9999)
        stress_login_data = {
            "userName": f"testuser{random_user_id}",
            "email": f"test{random_user_id}@example.com",
            "password": "test123"
        }
        
        with self.client.post(
            "/client_login",
            data=stress_login_data,
            catch_response=True
        ) as response:
            try:
                if "token" in response.json() or response.json()["msg"] == "In correct email or password":
                    response.success()
                else:
                    response.failure(f"Stress login failed: {response.json()}")
            except json.JSONDecodeError:
                response.failure("Invalid JSON response")
            except Exception as e:
                response.failure(f"Error: {str(e)}")

# BDD-style scenarios documentation
def test_load_scenario():
    """
    Given a Flask application is running
    When multiple users attempt to register and login
    Then the system should handle the load without errors
    And response times should remain under acceptable thresholds
    """
    pass  # Implemented through the UserBehavior class

def test_stress_scenario():
    """
    Given a Flask application is running
    When the system is under heavy login load
    Then it should maintain functionality
    And either serve requests or fail gracefully
    """
    pass  # Implemented through the StressTest class