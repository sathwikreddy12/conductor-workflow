from framework.conductor_script import ConductorWorker
from service import user_service

# Register SAME worker for BOTH tasks

worker_login = ConductorWorker(
    conductor_url="http://conductor-server:8080",
    task_name="login_task",
    worker_id="user-worker-login",
    handler=user_service
)

worker_logout = ConductorWorker(
    conductor_url="http://conductor-server:8080",
    task_name="logout_task",
    worker_id="user-worker-logout",
    handler=user_service
)

# Run both
import threading

threading.Thread(target=worker_login.poll).start()
threading.Thread(target=worker_logout.poll).start()
