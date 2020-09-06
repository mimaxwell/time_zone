FROM ubuntu:18.04
RUN apt-get update -y &&  apt-get install -y\
    python3.5 \
    python3-pip 
 # maybe want to install vim and tmux? 


WORKDIR /src

COPY requirements.txt /src/requirements.txt

RUN pip3 install -r requirements.txt
