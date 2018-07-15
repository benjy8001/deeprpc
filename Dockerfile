FROM debian:latest

RUN echo "deb http://deb.debian.org/debian jessie-backports main" >> /etc/apt/sources.list

RUN apt-get -y update && apt-get upgrade -y
RUN apt-get install -y python3 python3-dev python3-pip

# gmpy2 cryptography
RUN apt-get install -y build-essential apt-utils libffi-dev libssl-dev kmod vim tree config-package-dev

ARG URLPYPI
ENV URLPYPI='https://ugloo:OUI0FxtdlVlnobmZYnEC@srvupypi.ubiquitus.info'

RUN mkdir /shared

COPY . /shared/
COPY entrypoint-bootstrap.sh /entrypoint-bootstrap.sh
COPY entrypoint-node.sh /entrypoint-node.sh

RUN python3 -m pip install pip setuptools virtualenv --upgrade

RUN mkdir -p /mnt/ugloo/apps/ && \
    virtualenv -p $(which python3) /mnt/ugloo/apps/deeprpc && \
    echo "source /mnt/ugloo/apps/deeprpc/bin/activate" >> /root/.bashrc && \
    /mnt/ugloo/apps/deeprpc/bin/pip install pip setuptools --upgrade

RUN cd /shared && /mnt/ugloo/apps/deeprpc/bin/pip install --quiet -r requirements.txt --extra-index-url $URLPYPI/ugloo/prod --extra-index-url $URLPYPI/ugloo/preprod --extra-index-url $URLPYPI/joris.carrier/dev
RUN cd /shared && /mnt/ugloo/apps/deeprpc/bin/pip install --quiet -r requirements-testing.txt
RUN cd /shared && /mnt/ugloo/apps/deeprpc/bin/python setup.py develop

RUN apt install procps -y

VOLUME ["/shared"]
WORKDIR /shared