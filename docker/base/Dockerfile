FROM centos:6.8
MAINTAINER Parker <oss@dp.farm>

ARG pyver=py34
ARG dp_port=52848

ADD common /data/script/common
ADD python /data/script/python

RUN echo 'alias dp4p_start="/data/script/common/cmd/start"' >> ~/.bashrc && \
    echo 'alias dp4p_stop="/data/script/common/cmd/stop"' >> ~/.bashrc && \
    echo 'alias dp4p_restart="/data/script/common/cmd/restart"' >> ~/.bashrc && \
    chmod +x -R /data/script && \
    /data/script/common/prepare && \
    /data/script/common/node && \
    /data/script/python/$pyver && \
    /data/script/common/cleanup

EXPOSE $dp_port

