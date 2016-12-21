FROM why2pac/dp4p:base-py35-0.1
MAINTAINER Parker <oss@dp.farm>

ARG dpver

RUN dp-pip install pillow --global-option="build_ext" \
                          --global-option="--enable-zlib" \
                          --global-option="--enable-jpeg" \
                          --global-option="--enable-tiff" \
                          --global-option="--enable-freetype" \
                          --global-option="--enable-lcms" \
                          --global-option="--enable-webp" \
                          --global-option="--enable-webpmux"

RUN dp-pip install dp-tornado==$dpver
CMD ["/bin/bash", "/data/script/common/run"]
