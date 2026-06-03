FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y \
    git \
    curl \
    python3 \
    python3-pip \
    docker.io && \
    rm -rf /var/lib/apt/lists/*

USER jenkins

COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

RUN jenkins-plugin-cli \
    --plugin-file /usr/share/jenkins/ref/plugins.txt
