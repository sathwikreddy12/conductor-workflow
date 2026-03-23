def user_service(task):
    task_type = task.get("taskType")
    input_data = task.get("inputData", {})

    username = input_data.get("username") or input_data.get("user")
    password = input_data.get("password")

    print(f"[user_worker] Task received: {task_type}")

    # -----------------------------
    # LOGIN TASK
    # -----------------------------
    if task_type == "login_task":

        print(f"[user_worker] Login attempt for user: {username}")

        if username == "admin" and password == "1234":
            return {
                "login_status": "success",
                "user": username
            }
        else:
            return {
                "login_status": "failed",
                "user": username
            }

    # -----------------------------
    # LOGOUT TASK (COMPENSATION)
    # -----------------------------
    elif task_type == "logout_task":

        print(f"[user_worker] Logging out user: {username}")

        return {
            "logout_status": "success",
            "user": username
        }
