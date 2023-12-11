FROM ubuntu:latest

WORKDIR /app

RUN apt update && \ 
  apt install build-essential libtool software-properties-common -y && \
  add-apt-repository -y ppa:deadsnakes/ppa && \
  apt -y --no-install-recommends install libgl1 libglib2.0-0 python3.10 python3-pip python3-dev

RUN python3.10 -m pip install --upgrade pip==21.1.1
RUN python3.10 -m pip install numpy==1.23.5
RUN python3.10 -m pip install Cython 
RUN python3.10 -m pip install lap==0.4.0

COPY requirements.txt .
COPY ./track/ByteTrack/requirements.txt ./track/ByteTrack/requirements.txt


WORKDIR /app/track/ByteTrack
RUN python3.10 -m pip install -r requirements.txt
COPY ./track/ByteTrack/ .
RUN python3.10 setup.py develop

WORKDIR /app
RUN python3.10 -m pip install -r requirements.txt

COPY . .

CMD ["flask", "--app", "app", "run", "-h", "0.0.0.0", "-p", "8080"]

