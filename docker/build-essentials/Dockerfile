FROM tbhapi/base-user

ENV DOCKER_IMAGE=tbhapi/build-essentials

# Add repos for GCC 5
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test                  && \
    apt-get update -y                                                  && \
    apt-get install -y                                                    \
      build-essential                                                     \
      gcc-5                                                               \
      g++-5                                                               \
      git                                                                 \
      openssl                                                             \
      lib32z1-dev                                                         \
      libreadline-dev                                                     \
      libssl-dev                                                          \
      libxml2-dev                                                         \
      libxslt1-dev                                                        \
      python-virtualenv                                                   \
      nginx                                                               \
      gunicorn                                                            \
      supervisor                                                          \
      wget                                                             && \
    apt-file update -y                                                 && \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5 60      \
                        --slave /usr/bin/g++ g++ /usr/bin/g++-5        && \
    apt-file update -y
