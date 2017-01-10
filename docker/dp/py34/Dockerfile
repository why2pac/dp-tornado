FROM why2pac/dp4p:base-py34-0.1
MAINTAINER Parker <oss@dp.farm>

ARG dpver

RUN dp-pip install dp-tornado==$dpver
CMD ["/bin/bash", "/data/script/common/run"]
