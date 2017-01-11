FROM ubuntu:14.04
LABEL version="1.1"

MAINTAINER Alexey Manikin <alexey@beget.ru>

# Prepare environment
ENV DEBIAN_FRONTEND noninteractive

RUN chmod 755 / && \
  chmod 711 /etc && \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y sudo git htop vim wget python3-software-properties python-software-properties software-properties-common && \ 
  apt-get -y remove openjdk* && \
  add-apt-repository ppa:webupd8team/java && \
  apt-get update && \
  echo debconf shared/accepted-oracle-license-v1-1 select true | \
  sudo debconf-set-selections && \
  echo debconf shared/accepted-oracle-license-v1-1 seen true | \
  sudo debconf-set-selections && \
  apt-get install -y oracle-java8-installer && \
  export JAVA_HOME=/usr/lib/jvm/java-8-oracle && \
  echo "export JAVA_HOME=/usr/lib/jvm/java-8-oracle" >> /etc/bash.bashrc && \
  cd /home && \
  wget https://rrdp.ripe.net/certification/content/static/validator/rpki-validator-app-2.23-dist.tar.gz && \
  tar -xzvf /home/rpki-validator-app-2.23-dist.tar.gz && \
  rm -rf /home/rpki-validator-app-2.23-dist.tar.gz && \ 
  rm -rf /var/lib/apt/lists/*;  

ADD install_minit.sh /usr/local/sbin/install_minit.sh
RUN /bin/bash /usr/local/sbin/install_minit.sh

ADD startup.sh /etc/minit/startup
RUN chmod 755 /etc/minit/startup
CMD ["/sbin/minit"]
# EOF
