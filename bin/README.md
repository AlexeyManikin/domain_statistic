Site http://www.ris.ripe.net/source/bgpdump/

    apt-get install -y libbz2-dev
    cd /usr/src
    wget http://www.ris.ripe.net/source/bgpdump/libbgpdump-1.4.99.13.tgz
    tar -xf libbgpdump-1.4.99.13.tgz
    cd libbgpdump-1.4.99.13
    ./configure --prefix=/opt/libbgpdump
    mkdir /opt/libbgpdump
    mkdir /opt/libbgpdump/bin
    mkdir /opt/libbgpdump/includes
    mkdir /opt/libbgpdump/lib
    make
    cp libbgpdump.so /opt/libbgpdump/lib
    cp bgpdump /opt/libbgpdump/bin
    cp bgpdump_lib.h /opt/libbgpdump/includes

    cp libbgpdump.a /opt/libbgpdump/lib
    cp bgpdump_attr.h  /opt/libbgpdump/includes
    cp bgpdump_formats.h /opt/libbgpdump/includes

Run:
     /opt/libbgpdump/bin/bgpdump