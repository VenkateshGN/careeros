from locust import HttpUser, task, between
import uuid

class CareerOSUser(HttpUser):
    # Wait between 1 and 2.5 seconds between tasks to simulate realistic behavior
    wait_time = between(1.0, 2.5)

    def on_start(self):
        """Register and login to get JWT token for authenticated routes."""
        self.email = f"load_{uuid.uuid4()}@gmail.com"
        self.password = "password123"

        # 1. Register User
        self.client.post("/users/", json={
            "full_name": "Load Tester",
            "email": self.email,
            "password": self.password
        })

        # 2. Login User
        res = self.client.post("/auth/login", json={
            "email": self.email,
            "password": self.password
        })

        if res.status_code == 200:
            token = res.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {token}"}
        else:
            self.headers = {}

    @task(3)
    def test_dashboard_latency(self):
        self.client.get("/dashboard/user-analytics", headers=self.headers, name="/dashboard")

    @task(2)
    def test_job_search_latency(self):
        # Simulate Job Search fetching jobs (pagination)
        self.client.get("/jobs/?skip=0&limit=50", name="/jobs/")

    @task(1)
    def test_resume_upload_speed(self):
        file_content = b"Mock PDF Content" * 1024 # ~16KB mocked resume
        self.client.post("/resume/upload", headers=self.headers, files={"resume": ("resume.pdf", file_content, "application/pdf")}, name="/resume/upload")

    @task(1)
    def test_ai_mock_latency(self):
        # Mocking an AI call (our backend falls back to mock endpoints, so it's safe and fast!)
        self.client.post("/ai/job-matching", headers=self.headers, json={
            "resume_text": "Python React",
            "job_description": "We need Python"
        }, name="/ai/job-matching")
