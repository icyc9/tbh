FROM tbhapi/base

ENV DOCKER_IMAGE=tbhapi/base-user

RUN adduser --disabled-password                \
            user                            && \
    chown root:root /home/user/.bashrc      && \
    chown root:root /home/user/.bash_logout && \
    rm /home/user/.profile                  && \
    mv /home/user/.bashrc /home/user/.bashrc.orig

COPY .bash_profile        /home/user/
COPY .bashrc              /home/user/
COPY .gemrc               /home/user/
COPY .git-completion.bash /home/user/
COPY .git-prompt.bash     /home/user/

# use dotfiles for root
RUN rm /root/.profile                   && \
    mv /root/.bashrc /root/.bashrc.orig && \
    cp /home/user/.bashrc /root/.bashrc

# Say goodbye to sh (dash) forever
RUN rm /bin/sh           && \
    ln /bin/bash /bin/sh

WORKDIR /home/user
