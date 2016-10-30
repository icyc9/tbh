FROM ubuntu:trusty

ENV DOCKER_IMAGE=base \
    TERM=xterm-256color

# Upgrade packages
RUN apt-get update -y                            && \
    apt-get -o Dpkg::Options::="--force-confnew"    \
            dist-upgrade -y                      && \
    apt-get install -y                              \
      apt-file                                      \
      apt-utils                                     \
      software-properties-common                 && \
    apt-file update -y
