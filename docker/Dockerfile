FROM centos:6.8
MAINTAINER Parker <oss@dp.farm>

ARG pyver=py34
ARG dp_port=52848

ADD common /data/script/common
ADD python /data/script/python

RUN chmod +x -R /data/script && \
    /data/script/common/prepare && \
    /data/script/common/node && \
    /data/script/python/$pyver && \
    /data/script/common/cleanup

EXPOSE $dp_port

CMD ["/bin/bash", "/data/script/common/run"]
