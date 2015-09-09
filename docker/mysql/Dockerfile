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


# fix locales
ADD config/locales /var/lib/locales/supported.d/local
RUN locale-gen

# Prepare environment
ENV DEBIAN_FRONTEND noninteractive

ADD install_minit.sh /usr/local/sbin/install_minit.sh
RUN /bin/bash /usr/local/sbin/install_minit.sh

RUN apt-key adv --keyserver keys.gnupg.net --recv-keys 1C4CBDCDCD2EFD2A
RUN echo "deb http://repo.percona.com/apt quantal main" >> /etc/apt/sources.list.d/percona.list
RUN echo "deb-src http://repo.percona.com/apt quantal main" >> /etc/apt/sources.list.d/percona.list
RUN apt-get update
RUN apt-get install -y percona-server-server-5.6 percona-server-client-5.6

# libmysql
RUN apt-get install -y libmysqlclient16 libmysqlclient18 libmysqlclient18.1 libcap2 zip unzip unrar p7zip bzip2 gzip \
                     exim4 exim4-daemon-heavy libaio1 libwrap0 libreadline6 git

ADD config/my.cnf /etc/mysql/my.cnf

RUN addgroup --gid 950 mysql || true
RUN adduser --quiet --system --disabled-login --no-create-home --uid 950 --gid 950  mysql || true

RUN cd /root/ && \
    git clone -n https://github.com/AlexeyManikin/domain_statistic.git --depth 1 && \
    cd domain_statistic && \
    git checkout HEAD structure.sql && \
    cp /root/domain_statistic/structure.sql /root/structure.sql && \
    rm -rf /root/domain_statistic;

RUN mkdir -p /etc/minit
ADD startup.sh /etc/minit/startup
RUN chmod 755 /etc/minit/startup
CMD ["/sbin/minit"]
# EOF







