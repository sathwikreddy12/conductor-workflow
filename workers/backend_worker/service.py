from datetime import datetime

# 🔥 INTERNAL SWITCHES
SIMULATE_BACKEND_FAILURE = True   # ✅ change to True to test failure

def backend_service(task):
    task_type = task.get("taskType")
    input_data = task.get("inputData", {})

    user = input_data.get("user")
    login_status = input_data.get("login_status")

    print(f"[backend_worker] Task: {task_type}")

    # -----------------------------
    # BACKEND TASK
    # -----------------------------
    if task_type == "backend_task":

        # 🔥 Simulated failure
        if SIMULATE_BACKEND_FAILURE:
            print("[backend_worker] 🚨 Simulated BACKEND FAILURE")
            return {"backend_status": "failed"}

        if login_status != "success":
            return {"backend_status": "failed"}

        print(f"[backend_worker] Processing user: {user}")

        return {
            "backend_status": "success",
            "user_record": {
                "user": user,
                "role": "standard_user",
                "processed_at": datetime.utcnow().isoformat()
            }
        }

    # -----------------------------
    # UNDO BACKEND
    # -----------------------------
    elif task_type == "undo_backend_task":

        print(f"[backend_worker] Rolling back backend for user: {user}")

        return {
            "undo_backend_status": "success",
            "user": user
        }
