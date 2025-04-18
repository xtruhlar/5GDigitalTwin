FROM ubuntu:jammy AS builder

ENV DEBIAN_FRONTEND=noninteractive

# Install updates and dependencies
RUN apt-get update && \
    apt-get -y install \
        make \
        g++ \
        libsctp-dev \
        lksctp-tools \
        git \
        vim \
        iproute2 \
        iptables \
        net-tools \
        ifupdown \
        iputils-ping \
        wget \
        libssl-dev \
        cmake

# Clone repo and checkout tag first
RUN git clone https://github.com/aligungr/UERANSIM

# Zmena task.cpp a task.hpp pre posielanie release signálu po odpojení UE
COPY ./task.cpp /UERANSIM/src/gnb/rls/task.cpp
COPY ./task.hpp /UERANSIM/src/gnb/ngap/task.hpp

# Build
RUN cd /UERANSIM && make -j$(nproc)


# Build final image
FROM ubuntu:jammy

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libsctp-dev \
        lksctp-tools \
        iproute2 \
        iptables \
        netbase \
        ifupdown \
        net-tools \
        iputils-ping && \
    apt-get autoremove -y && apt-get autoclean
    
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        curl \
        iperf3 && \
    apt-get clean

RUN pip3 install prometheus_client


COPY --from=builder /UERANSIM/build /UERANSIM/build
COPY --from=builder /UERANSIM/config /UERANSIM/config

# Set the working directory to UERANSIM
WORKDIR /UERANSIM/build

COPY ueransim_image_init.sh /
CMD ["/bin/bash", "-c", "/ueransim_image_init.sh"]

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.