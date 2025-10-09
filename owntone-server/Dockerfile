FROM ubuntu:20.04

# Install common dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && \
    apt-get -y install sudo \ 
    apt-utils \
    build-essential \
    openssl \
    clang \
    graphviz-dev \
    git \
    autoconf \
    libgnutls28-dev \
    llvm \
    python3-pip \
    nano \
    net-tools \
    vim \
    gdb \
    netcat \
    strace \
    wget
RUN apt-get -y install \
    bison \
    flex \
    autotools-dev autoconf automake libtool gettext gawk \
    gperf antlr3 libantlr3c-dev libconfuse-dev libunistring-dev libsqlite3-dev \
    libavcodec-dev libavformat-dev libavfilter-dev libswscale-dev libavutil-dev \
    libasound2-dev libxml2-dev libgcrypt20-dev libavahi-client-dev zlib1g-dev \
    libevent-dev libplist-dev libsodium-dev libjson-c-dev libwebsockets-dev \
    libcurl4-openssl-dev libprotobuf-c-dev avahi-daemon

# Add a new user ubuntu, pass: ubuntu
RUN groupadd ubuntu && \
    useradd -rm -d /home/ubuntu -s /bin/bash -g ubuntu -G sudo -u 1000 ubuntu -p "$(openssl passwd -1 ubuntu)"

RUN chmod 777 /tmp

# Use ubuntu as default username
USER ubuntu
WORKDIR /home/ubuntu

# Set up working directory
ENV WORKDIR="/home/ubuntu/experiments"
RUN mkdir $WORKDIR

# Copy the necessary patch to run on this ubuntu 20.04 container
COPY --chown=ubuntu:ubuntu owntone.patch ${WORKDIR}/owntone.patch

# Copy other needed files
RUN mkdir ${WORKDIR}/MP3
COPY --chown=ubuntu:ubuntu owntone.conf ${WORKDIR}/owntone.conf

# Download and compile owntone
RUN cd $WORKDIR && \
    git clone https://github.com/owntone/owntone-server.git owntone && \
    cd owntone && \
    git checkout 334beb1 && \
    patch -p1 < $WORKDIR/owntone.patch && \
    autoreconf -i && \
    CC=clang CFLAGS="-DSQLITE_CORE -O0 -g" ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var  --disable-mpd --disable-itunes --disable-lastfm --disable-spotify --disable-verification  --disable-shared --enable-static && \
    make clean all

# Setting up the environment using root account
USER root

RUN touch /home/ubuntu/experiments/owntone.log && \
    chown ubuntu.root /home/ubuntu/experiments/owntone.log

RUN touch /var/log/owntone.log && \
    chown ubuntu.root /var/log/owntone.log

RUN touch /var/run/owntone.pid && \
    chown ubuntu.root /var/run/owntone.pid

RUN update-rc.d avahi-daemon defaults

RUN mkdir /usr/share/owntone/ && \
    cp -R $WORKDIR/owntone/htdocs /usr/share/owntone/htdocs

RUN ln -s $WORKDIR/MP3 /tmp/MP3

#The script needs to launch dbus and avahi-daemon using sudo
RUN echo "ALL ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Switch back to ubuntu account
USER ubuntu
RUN mkdir ${WORKDIR}/db
