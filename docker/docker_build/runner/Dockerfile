FROM ubuntu:14.04

MAINTAINER Alexey Manikin <alexey@beget.ru>

# prepare environment
ENV DEBIAN_FRONTEND noninteractive
ENV APT_GET_INSTALL apt-get install --no-install-recommends -qq -y

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E007F6BD && \
    echo "deb http://ppa.launchpad.net/chazomaticus/minit/ubuntu trusty main" > /etc/apt/sources.list.d/minit.list

# setup msk timezone
RUN rm -f /etc/localtime && ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime && chmod 644 /etc/localtime

# update package list
RUN apt-get update -qq

# dist upgrade
RUN apt-get dist-upgrade -qq -y

# install base utils and service
RUN $APT_GET_INSTALL minit  wget curl git less psmisc build-essential cron pdns-recursor

# install python
RUN $APT_GET_INSTALL libpython2.7 python python-pip python-all-dev python-subnettree python-psutil python-mysqldb &&\
    pip install dnspython && \
    pip install pillow && \
    pip install --upgrade psutil

# install code
RUN mkdir -p /home/domain_statistic && \
    git clone -b master -- https://github.com/AlexeyManikin/domain_statistic.git /home/domain_statistic && \
    rm -rf /home/domain_statistic/.git && \
    rm -rf /home/domain_statistic/docker && \
    mkdir /home/domain_statistic/download

# make dir
RUN mkdir -p /etc/minit

# add user
RUN addgroup --gid 950 runner
RUN adduser --quiet --system --disabled-login --no-create-home --uid 950 --gid 950  runner

# add file
ADD recursor.conf /etc/powerdns/recursor.conf
ADD init.sh /etc/minit/startup
ADD cron /var/spool/cron/crontabs/runner

# fix permition
RUN chmod 755 /etc/minit/startup && \
    chown runner.runner /var/spool/cron/crontabs/runner && \
    chown runner.runner /home/domain_statistic -R && \
    chmod 755 /etc/minit/startup

CMD ["/sbin/minit"]
# EOF
