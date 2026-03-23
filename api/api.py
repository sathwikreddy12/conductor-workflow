import requests
import time
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

CONDUCTOR_URL = "http://conductor-server:8080/api"

# -----------------------------
# Request Model
# -----------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


# -----------------------------
# Start Workflow
# -----------------------------
def start_workflow(username, password):
    payload = {
        "name": "service_flow",
        "version": 1,
        "input": {
            "username": username,
            "password": password
        }
    }

    response = requests.post(
        f"{CONDUCTOR_URL}/workflow",
        json=payload
    )

    return response.text.strip().replace('"', '')


# -----------------------------
# Wait + Analyze Workflow (FINAL FIXED)
# -----------------------------
def wait_for_completion(workflow_id, timeout=20):

    waited = 0

    while waited < timeout:

        response = requests.get(
            f"{CONDUCTOR_URL}/workflow/{workflow_id}?includeTasks=true"
        )

        data = response.json()
        status = data.get("status")

        if status == "COMPLETED":

            tasks = data.get("tasks", [])

            login_status = None
            backend_status = None
            db_status = None

            print("\n===== DEBUG TASK DUMP =====")
            for t in tasks:
                print(
                    "REF:", t.get("referenceTaskName"),
                    "| STATUS:", t.get("status"),
                    "| OUTPUT:", t.get("outputData")
                )
            print("===========================\n")

            for task in tasks:

                ref = task.get("referenceTaskName")
                output = task.get("outputData") or {}

                # ✅ capture only once
                if ref == "login" and login_status is None:
                    login_status = output.get("login_status")

                elif ref == "backend" and backend_status is None:
                    backend_status = output.get("backend_status")

                elif ref == "database" and db_status is None:
                    db_status = output.get("db_status")

            print("\n===== FINAL ANALYSIS =====")
            print("LOGIN:", login_status)
            print("BACKEND:", backend_status)
            print("DB:", db_status)
            print("==========================\n")

            return {
                "status": "COMPLETED",
                "login_status": login_status,
                "backend_status": backend_status,
                "db_status": db_status
            }

        elif status in ["FAILED", "TERMINATED"]:
            return {"status": "FAILED"}

        time.sleep(1)
        waited += 1

    return {"status": "TIMEOUT"}


# -----------------------------
# API Endpoint (FINAL)
# -----------------------------
@app.post("/login")
def login(request: LoginRequest):

    try:
        workflow_id = start_workflow(request.username, request.password)

        result = wait_for_completion(workflow_id)

        if result["status"] == "COMPLETED":

            login_status = result.get("login_status")
            backend_status = result.get("backend_status")
            db_status = result.get("db_status")

            print("\n===== API DECISION =====")
            print("LOGIN:", login_status)
            print("BACKEND:", backend_status)
            print("DB:", db_status)
            print("========================\n")

            # ❌ LOGIN FAILED
            if login_status != "success":
                return {"message": "Invalid username or password"}

            # ❌ BACKEND FAILED
            if backend_status != "success":
                return {"message": "Backend service failed, user logged out"}

            # ❌ DB FAILED
            if backend_status == "success" and db_status != "success":
                return {"message": "Database error, rollback completed"}

            # ✅ SUCCESS
            return {
                "message": "User login successful",
                "user": request.username
            }

        elif result["status"] == "FAILED":
            return {"message": "Workflow execution failed"}

        else:
            return {"message": "Request timeout"}

    except Exception as e:
        return {
            "message": "Error occurred",
            "error": str(e)
        }
