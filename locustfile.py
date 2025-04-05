from locust import HttpUser, task, between


class FastAPIUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def get_statistics(self):
        user_id = 5105116164  # Пример юзера
        self.client.get(f"/statistics/{user_id}")

    @task
    def post_sleep(self):
        self.client.post("/sleep/", json={"user_telegram_id": 747408444, "hours": 2})
