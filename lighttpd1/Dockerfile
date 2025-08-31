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
    libssl-dev \
    llvm \
    python3-pip \
    nano \
    net-tools \
    vim \
    gdb \
    netcat \
    strace \
    libcap-dev \
    libpcre2-dev \
    libpcre2-8-0 \
    libcurl4-openssl-dev \
    libjson-c-dev \
    pkg-config \
    zlib1g-dev \
    automake libtool m4 \
    wget

# Add a new user ubuntu, pass: ubuntu
RUN groupadd ubuntu && \
    useradd -rm -d /home/ubuntu -s /bin/bash -g ubuntu -G sudo -u 1000 ubuntu -p "$(openssl passwd -1 ubuntu)"

RUN chmod 777 /tmp

# Use ubuntu as default username
USER ubuntu
WORKDIR /home/ubuntu

# Import environment variable to pass as parameter to make (e.g., to make parallel builds with -j)
ARG MAKE_OPT

# Set up environment variables
ENV WORKDIR="/home/ubuntu/experiments"

RUN mkdir $WORKDIR

# Set up environment variables for ASAN
ENV ASAN_OPTIONS='abort_on_error=1:symbolize=0:detect_leaks=0:detect_stack_use_after_return=1:detect_container_overflow=0:poison_array_cookie=0:malloc_fill_byte=0:max_malloc_fill_size=16777216'

# Download and compile Lighttpd1.4
RUN cd $WORKDIR && \
    git clone https://git.lighttpd.net/lighttpd/lighttpd1.4.git lighttpd1 && \
    cd lighttpd1 && \
    git checkout 9f38b63 && \
    ./autogen.sh && \ 
    CC=clang CXX=clang++ ./configure --enable-static --disable-shared && \
    sed -i.bak '/^CFLAGS =\|^CFLAGS_FOR_BUILD =/ {
        s/-g -O2/-g -O0 -fsanitize=address/
    }' src/Makefile
    make clean all $MAKE_OPT || make all

COPY --chown=ubuntu:ubuntu inputs ${WORKDIR}/inputs
COPY --chown=ubuntu:ubuntu lighttpd.conf ${WORKDIR}/lighttpd.conf

RUN cp -rf ${WORKDIR}/inputs/* /tmp/
