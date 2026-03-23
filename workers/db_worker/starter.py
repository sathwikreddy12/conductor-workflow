from framework.conductor_script import ConductorWorker
from service import db_service
import threading

worker_db = ConductorWorker(
    conductor_url="http://conductor-server:8080",
    task_name="db_task",
    worker_id="db-worker-main",
    handler=db_service
)

worker_undo = ConductorWorker(
    conductor_url="http://conductor-server:8080",
    task_name="undo_db_task",
    worker_id="db-worker-undo",
    handler=db_service
)

threading.Thread(target=worker_db.poll).start()
threading.Thread(target=worker_undo.poll).start()
