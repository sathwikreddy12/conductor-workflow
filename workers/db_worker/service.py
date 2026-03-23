DATABASE = []

# 🔥 INTERNAL SWITCHES
SIMULATE_DB_FAILURE = False   # ✅ change to True to test failure

def db_service(task):
    task_type = task.get("taskType")
    input_data = task.get("inputData", {})

    print(f"[db_worker] Task: {task_type}")

    # -----------------------------
    # DB TASK
    # -----------------------------
    if task_type == "db_task":

        # 🔥 Simulated failure
        if SIMULATE_DB_FAILURE:
            print("[db_worker] 🚨 Simulated DB FAILURE")
            return {"db_status": "failed"}

        user_record = input_data.get("user_record")

        if not user_record:
            return {"db_status": "failed"}

        DATABASE.append(user_record)

        print(f"[db_worker] Stored: {user_record}")
        print(f"[db_worker] Current DB: {DATABASE}")

        return {
            "db_status": "success",
            "user": user_record.get("user")
        }

    # -----------------------------
    # UNDO DB
    # -----------------------------
    elif task_type == "undo_db_task":

        user = input_data.get("user")

        print(f"[db_worker] Rolling back DB for user: {user}")

        global DATABASE
        DATABASE = [u for u in DATABASE if u.get("user") != user]

        print(f"[db_worker] DB after rollback: {DATABASE}")

        return {
            "undo_db_status": "success",
            "user": user
        }
