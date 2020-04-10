FROM openjdk:8-jre-alpine

RUN apk add rsync
RUN wget https://ftp.ripe.net/tools/rpki/validator3/prod/generic/rpki-validator-3-latest-dist.tar.gz && mkdir -p /var/lib/rpki-validator-3

WORKDIR /var/lib/rpki-validator-3

RUN tar xfz /rpki-validator-3-latest-dist.tar.gz; mv */* .;
RUN sed -i 's/env bash/env ash/g'  rpki-validator-3.sh
RUN sed -i 's/server.address=localhost/server.address=0.0.0.0/g' conf/application.properties
RUN sed -i '/MEM_OPTIONS=/c\MEM_OPTIONS="-Xms$JVM_XMS -Xmx$JVM_XMX -XX:+ExitOnOutOfMemoryError -XX:+UseContainerSupport"' rpki-validator-3.sh

CMD ["/var/lib/rpki-validator-3/rpki-validator-3.sh"]
# EOF
