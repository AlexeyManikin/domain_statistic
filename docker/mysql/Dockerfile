FROM mariadb

MAINTAINER Alexey Manikin <alexey@beget.ru>
LABEL version="1.2"

RUN cat /usr/local/bin/docker-entrypoint.sh

# chmod a+x / in container init start
RUN sed -i 's#set -eo pipefail#set -eo pipefail; if [ "$EUID" -eq 0 ] ; then chmod a+x / ; fi#g' /usr/local/bin/docker-entrypoint.sh
