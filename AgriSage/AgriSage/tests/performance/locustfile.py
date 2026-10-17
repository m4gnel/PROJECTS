from locust import HttpUser, task, between


class AgriSAGEFarmerUser(HttpUser):
    wait_time = between(2, 8)

    def on_start(self):
        resp = self.client.post(
            "/api/v1/auth/verify-otp",
            json={"phone": "+919999999999", "otp": "123456"}
        )
        if resp.status_code == 200:
            token = resp.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {token}"}
        else:
            self.headers = {}

    @task(3)
    def get_farms(self):
        self.client.get("/api/v1/farms", headers=self.headers)

    @task(2)
    def get_weather(self):
        self.client.get("/api/v1/weather/10.12/76.34", headers=self.headers)

    @task(1)
    def generate_advisory(self):
        self.client.post(
            "/api/v1/diagnose",
            json={"observation_id": "test-obs-id"},
            headers=self.headers
        )
