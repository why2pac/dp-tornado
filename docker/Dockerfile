FROM centos:6.8
MAINTAINER Parker <oss@dp.farm>

ARG pyver=py34
ARG port=52848

ADD common /data/script/common
ADD python /data/script/python

RUN chmod +x -R /data/script && \
    /data/script/common/prepare && \
    /data/script/python/$pyver && \
    /data/script/common/cleanup

RUN yum install -y telnet

EXPOSE $port
CMD ["/bin/bash", "/data/script/common/run"]
