FROM python:3.10

WORKDIR /app

COPY workers/login_worker/requirements.txt .

RUN pip install -r  requirements.txt 

COPY workers/login_worker/ .

COPY workers/framework ./framework

CMD ["python" ,"-u" ,  "starter.py"]



