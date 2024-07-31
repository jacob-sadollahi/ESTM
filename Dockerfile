FROM python:3.11.1-slim-bullseye
ARG TARGETPLATFORM
RUN echo "I'm building for $TARGETPLATFORM"
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --allow-releaseinfo-change && apt-get upgrade -y && apt-get install -qqy \
    curl \
    wget \
    apt-utils \
    libssl-dev \
    openssh-server \
    build-essential  \
    python3-dev \
    libx11-6\
    libxext-dev \
    libxrender-dev \
    libxinerama-dev \
    libxi-dev \
    libxrandr-dev \
    libxcursor-dev \
    libxtst-dev \
    python3-tk && rm -rf /var/lib/apt/lists/*

RUN mkdir /var/run/sshd \
  && echo 'root:screencast' | /usr/sbin/chpasswd \
  && sed -i '/PermitRootLogin/c\PermitRootLogin yes' /etc/ssh/sshd_config \
  && sed -i '/AllowTcpForwarding/c\AllowTcpForwarding yes' /etc/ssh/sshd_config \
  # SSH login fix. Otherwise user is kicked off after login
  && sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /usr/sbin/sshd \
  && echo "export VISIBLE=now" >> /etc/profile \
  && ssh-keygen -A
ENV NOTVISIBLE "in users profile"

RUN mkdir -p /app | \
    mkdir -p /media-files

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

COPY ./scripts/* /scripts/
RUN chmod +x /scripts/*

WORKDIR /app

# Set the display port to avoid crash and to be able to use the container with a remote host
ENV DISPLAY=:0
CMD export DISPLAY =":0"

EXPOSE 22
