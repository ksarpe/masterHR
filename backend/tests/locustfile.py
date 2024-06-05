from locust import HttpUser, TaskSet, task, between

class ProcessImage(TaskSet):
    @task
    def send_image(self):
        # Przygotuj dane do wysłania (przykładowy obraz)
        with open("ILoveYou.png", "rb") as image_file:
            files = {'file': image_file}
            self.client.post("/process_frame", files=files)

class WebsiteUser(HttpUser):
    tasks = [ProcessImage]
    wait_time = between(0.5, 1)

# Jeśli chcesz przetestować więcej niż jeden endpoint, możesz dodać kolejne taski w klasie UserBehavior
