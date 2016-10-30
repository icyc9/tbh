FROM tbhapi/build-essentials

ENV DOCKER_IMAGE=tbhapi/python-3.5.1

ENV PATH=/usr/local/bin:$PATH

RUN wget -O -                                                     \
      https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz |  \
    tar xz                                                     && \
    cd Python-3.5.1                                            && \
    ./configure                                                && \
    make install

RUN rm -rf Python-3.5.1                  && \
    cd /usr/local/bin                    && \
    ln -s idle3.5 idle                   && \
    ln -s pip3.5 pip                     && \
    ln -s python3.5 python               && \
    ln -s pydoc3.5 pydoc                 && \
    ln -s python3.5-config python-config
