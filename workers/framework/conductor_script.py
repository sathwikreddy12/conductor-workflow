import time
import requests

class ConductorWorker:

    def __init__(self, conductor_url, task_name, worker_id, handler):
        self.conductor_url = conductor_url  # e.g., http://conductor-server:8080
        self.task_name = task_name
        self.worker_id = worker_id
        self.handler = handler

    def poll(self):
        while True:
            try:
                # Poll task
                response = requests.get(
                    f"{self.conductor_url}/api/tasks/poll/{self.task_name}?workerid={self.worker_id}"
                )

                if response.status_code != 200 or not response.text.strip():
                    time.sleep(2)
                    continue

                task = response.json()

                if task and "taskId" in task:
                    task_id = task["taskId"]
                    print(f"[{self.worker_id}] Received task '{self.task_name}' (ID: {task_id})")

                    # Call the handler to process the task
                    result = self.handler(task)

                    # Ensure outputData is a dict
                    if isinstance(result, dict):
                        output = result.get("output", result)
                    else:
                        output = {}

                    # Task completion payload
                    update = {
                        "taskId": task_id,
                        "workflowInstanceId": task["workflowInstanceId"],
                        "status": "COMPLETED",
                        "outputData": output
                    }

                    # Post to correct endpoint (v3+)
                    r = requests.post(f"{self.conductor_url}/api/tasks", json=update)
                    if r.status_code == 200:
                        print(f"[{self.worker_id}] Completed task: {self.task_name}")
                    else:
                        print(f"[{self.worker_id}] Failed to complete task: {r.text}")

            except Exception as e:
                print(f"[{self.worker_id}] Worker error:", e)

            time.sleep(2)
