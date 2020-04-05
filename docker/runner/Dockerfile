FROM ubuntu:18.04
LABEL version="1.2"
MAINTAINER Alexey Manikin <alexey@beget.ru>

# Prepare environment
ENV DEBIAN_FRONTEND noninteractive

# Install.
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y rsyslog libpython3.6 python3.6 python3-pip && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y byobu curl htop man unzip vim wget git build-essential cron && \
  apt-get install --no-install-recommends -qq -y python3-all-dev python3-subnettree \
                    python3-mysqldb python3-psutil && \
  pip3 install dnspython && \
  pip3 install --upgrade psutil && \
  pip3 install prettytable && \
  apt-get clean && \
  rm -rf /etc/localtime && \
  ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
  apt-get install -y tzdata && \
  rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*;

# need for developing
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /root/.ssh;

ADD config/sshd_config /etc/ssh/sshd_config
ADD config/authorized_keys /root/.ssh/authorized_keys

ADD install_code.sh /usr/local/sbin/install_code.sh
RUN /bin/bash /usr/local/sbin/install_code.sh

ADD init.sh /sbin/startup.sh
RUN chmod 755 /sbin/startup.sh

CMD ["/sbin/startup.sh"]
# EOF
