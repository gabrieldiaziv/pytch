FROM ubuntu:latest

WORKDIR /app

RUN apt update && \ 
  apt -y --no-install-recommends install libgl1 libglib2.0-0 python3 python3-pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "--app", "app", "run", "-h", "0.0.0.0", "-p", "8080"]

