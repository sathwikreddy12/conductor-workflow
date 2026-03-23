from framework.conductor_script import ConductorWorker
from service import backend_service
import threading

worker_backend = ConductorWorker(
    conductor_url="http://conductor-server:8080",
    task_name="backend_task",
    worker_id="backend-worker-main",
    handler=backend_service
)

worker_undo = ConductorWorker(
    conductor_url="http://conductor-server:8080",
    task_name="undo_backend_task",
    worker_id="backend-worker-undo",
    handler=backend_service
)

threading.Thread(target=worker_backend.poll).start()
threading.Thread(target=worker_undo.poll).start()
