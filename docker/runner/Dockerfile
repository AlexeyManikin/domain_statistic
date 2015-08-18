FROM ubuntu:14.04
LABEL version="1.0"

MAINTAINER Alexey Manikin <alexey@beget.ru>

# Install.
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y byobu curl git htop man unzip vim wget && \
  rm -rf /var/lib/apt/lists/*

# Prepare environment
ENV DEBIAN_FRONTEND noninteractive

# This is roughly equivalent to add-apt-repository ppa:chazomaticus/minit.
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E007F6BD
RUN echo "deb http://ppa.launchpad.net/chazomaticus/minit/ubuntu quantal main" > /etc/apt/sources.list.d/minit.list
RUN apt-get update && apt-get upgrade -y && apt-get install -y minit # etc.

RUN  apt-get install --no-install-recommends -qq -y git build-essential cron libpython2.7 python python-pip \
                    python-all-dev python-subnettree \
                    python-mysqldb python-psutil && \
    pip install dnspython && \
    pip install --upgrade psutil

RUN mkdir -p /home/domain_statistic && \
    git clone -b master -- https://gitlab.beget.ru/amanikin/domain_statictic.git /home/domain_statistic && \
    rm -rf /home/domain_statistic/.git && \
    rm -rf /home/domain_statistic/docker && \
    mkdir /home/domain_statistic/download && \
    echo 4

RUN mkdir -p /etc/minit

ADD init.sh /etc/minit/startup
CMD ["/sbin/minit"]
# EOF
