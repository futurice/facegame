########################################
#	Docker installation for Facegame   #
########################################

FROM ubuntu:12.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    git \
    libxml2-dev \
    python \
    build-essential \
    make \
    gcc \
    python-dev \
    locales \
    python-pip \
    npm \
    curl \
    software-properties-common \
    libfreetype6 \
    libfontconfig

#	Installing virtualenv
RUN pip install virtualenv

#	Runing virtualenv
RUN virtualenv --no-site-packages /opt/ve/facegame

#	Installing phantomjs
RUN curl -L https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-linux-x86_64.tar.bz2 | \
    tar -C /usr/local -xjf - && ln -sf ../phantomjs-1.9.7-linux-x86_64/bin/phantomjs /usr/local/bin/

#	Installing casperjs
RUN git clone git://github.com/n1k0/casperjs.git /usr/local/casperjs && \
    ln -sf ../casperjs/bin/casperjs /usr/local/bin

ADD . /opt/apps/facegame

#	Open port 8000
EXPOSE 8000

CMD cd /opt/apps/facegame && \
    git remote rm origin && \
    git remote add origin https://github.com/futuriceit/facegame.git && \
    git pull origin master && \
    /opt/ve/facegame/bin/pip install -r requirements.txt && \
    bash