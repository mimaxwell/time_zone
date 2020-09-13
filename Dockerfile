FROM ubuntu:20.04

RUN apt-get update -y &&  apt-get install -y\
#     python3.7.0 \
     python3-pip 
 


WORKDIR /src

COPY requirements.txt /src/requirements.txt

RUN pip3 install -r requirements.txt
