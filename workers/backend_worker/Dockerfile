FROM python:3.10

WORKDIR /app

COPY workers/backend_worker/requirements.txt .

RUN pip install -r requirements.txt

COPY workers/backend_worker/ .

COPY workers/framework ./framework 

CMD ["python" , "-u" , "starter.py"]



