FROM ubuntu:jammy

ENV DEBIAN_FRONTEND=noninteractive

# Install updates and dependencies
RUN apt-get update && \
    apt-get -y install wget git clang llvm gcc-multilib libbpf-dev \
    net-tools iputils-ping git ifupdown iperf iptables

# Install Golang
RUN rm -rf /usr/local/go && wget https://go.dev/dl/go1.22.4.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.22.4.linux-amd64.tar.gz

ENV PATH="/usr/local/go/bin:${PATH}"

# Install the Swag command line tool for Golang
RUN go install github.com/swaggo/swag/cmd/swag@v1.8.12

# Get eupf, compile and install
RUN export PATH=$(go env GOPATH)/bin:${PATH} && \
    git clone https://github.com/edgecomllc/eupf.git && \
    cd eupf && git checkout tags/v0.6.4 && \
    go generate -v ./cmd/... && \
    go build -v -o bin/eupf ./cmd/

# Set the working directory to eupf
WORKDIR /eupf

CMD ["/bin/bash", "-c", "/mnt/eupf/eupf_init.sh"]

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.