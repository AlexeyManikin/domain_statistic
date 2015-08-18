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


# Install pdns-recursor
RUN apt-get install --no-install-recommends -qq -y build-essential pdns-recursor
ADD config/recursor.conf /etc/powerdns/recursor.conf

RUN mkdir -p /etc/minit
ADD startup.sh /etc/minit/startup
RUN chmod 755 /etc/minit/startup
CMD ["/sbin/minit"]
# EOF