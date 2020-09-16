# vim:set ft=dockerfile:

####
# base_image - Bare bones image with the base packages needed to run Saabaza_Web_App
####

FROM debian:10.3-slim as base_image

LABEL maintainer="Roberto Rosario roberto.rosario@Saabaza_Web_App.com"

COPY config.env /config.env

ENV PYTHONUNBUFFERED=1 \
    LC_ALL=C.UTF-8 \
    PROJECT_INSTALL_DIR=/opt/Saabaza_Web_App

# Debian package caching
ARG APT_PROXY
RUN set -x \
&& if [ "${APT_PROXY}" ]; \
    then echo "Acquire::http { Proxy \"http://${APT_PROXY}\"; };" > /etc/apt/apt.conf.d/01proxy \
; fi \
# Install base OS packages to run Saabaza_Web_App
&& DEBIAN_FRONTEND=noninteractive \
apt-get update \
&& apt-get install -y --no-install-recommends \
    ca-certificates \
    exiftool \
    fonts-arphic-uming \
    fonts-arphic-ukai \
    fonts-unfonts-core \
    ghostscript \
    git-core \
    gpgv \
    gnupg1 \
    graphviz \
    libfuse2 \
    libmagic1 \
    libmariadb3 \
    libpq5 \
    libreoffice \
    poppler-utils \
    python3-distutils \
    sane-utils \
    sudo \
    supervisor \
    tesseract-ocr \
# Remove make and build dependencies
&& apt-get remove make libproxy-tools libreoffice-avmedia-backend-vlc libvlc-bin libvlc5 libvlccore9 adwaita-icon-theme gsettings-desktop-schemas libgstreamer-plugins-base1.0-0 -y \
&& apt-get autoremove -y --purge \
# Add appsaabaza user
&& adduser appsaabaza --disabled-password --disabled-login --no-create-home --gecos "" \
# Pillow can't find zlib or libjpeg on aarch64 (ODROID C2)
&& if [ "$(uname -m)" = "aarch64" ]; then \
    ln -s /usr/lib/aarch64-linux-gnu/libz.so /usr/lib/ \
    && ln -s /usr/lib/aarch64-linux-gnu/libjpeg.so /usr/lib/ \
; fi \
# Pillow can't find zlib or libjpeg on armv7l (ODROID HC1)
&& if [ "$(uname -m)" = "armv7l" ]; then \
    ln -s /usr/lib/arm-linux-gnueabihf/libz.so /usr/lib/ \
    && ln -s /usr/lib/arm-linux-gnueabihf/libjpeg.so /usr/lib/ \
; fi

####
# builder_image - This image builds the Python package and is discarded afterwards
#                 only the build artifact is carried over to the next image.
####

# Reuse image
FROM base_image as builder_image

# Python libraries caching
ARG PIP_INDEX_URL
ARG PIP_TRUSTED_HOST

WORKDIR /src

# Copy the source files needed to build the Python package
COPY --chown=appsaabaza:appsaabaza requirements /src/requirements
COPY --chown=appsaabaza:appsaabaza \
    HISTORY.rst \
    LICENSE \
    MANIFEST.in \
    README.md \
    README.rst \
    setup.py \
    /src/

COPY --chown=appsaabaza:appsaabaza appsaabaza /src/appsaabaza

# Install development packages needed to build the Python packages
RUN DEBIAN_FRONTEND=noninteractive \
apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    libpq-dev \
    libtiff-dev \
    zlib1g-dev \
    libssl-dev \
    g++ \
    gcc \
    python3-dev \
    python3-venv \
&& mkdir -p "${PROJECT_INSTALL_DIR}" \
&& chown -R appsaabaza:appsaabaza "${PROJECT_INSTALL_DIR}" \
&& chown -R appsaabaza:appsaabaza /src

USER appsaabaza

RUN set -a \
&& . /config.env \
&& set +a \
&& python3 -m venv "${PROJECT_INSTALL_DIR}" \
&& . "${PROJECT_INSTALL_DIR}/bin/activate" \
&& pip install --no-cache-dir \
    amqp==$PYTHON_AMQP_VERSION \
    mysqlclient==$PYTHON_MYSQL_VERSION \
    psycopg2==$PYTHON_PSYCOPG2_VERSION \
    redis==$PYTHON_REDIS_VERSION \
    flower==$PYTHON_FLOWER_VERSION \
# psutil is needed by ARM builds otherwise gevent and gunicorn fail to start
&& UNAME=`uname -m` && if [ "${UNAME#*arm}" != $UNAME ]; then \
    pip install --no-cache-dir \
    psutil==$PYTHON_PSUTIL_VERSION \
; fi \
# Install the Python packages needed to build Saabaza_Web_App
&& pip install --no-cache-dir -r /src/requirements/build.txt \
# Build Saabaza_Web_App
&& python3 setup.py sdist \
# Install the built Saabaza_Web_App package
&& pip install --no-cache-dir dist/appsaabaza* \
# Install the static content
&& Saabaza_Web_App.py installdependencies \
&& APPSAABAZA_STATIC_ROOT=${PROJECT_INSTALL_DIR}/static Saabaza_Web_App.py preparestatic --link --noinput

COPY --chown=appsaabaza:appsaabaza requirements/testing-base.txt "${PROJECT_INSTALL_DIR}"

####
# Final image - base_image + builder_image artifact (Appsaabazainstall directory)
####

FROM base_image

COPY --from=builder_image --chown=appsaabaza:appsaabaza "${PROJECT_INSTALL_DIR}/" "${PROJECT_INSTALL_DIR}/"

USER root

COPY docker/rootfs /

VOLUME ["/var/lib/appsaabaza"]

ENTRYPOINT ["entrypoint.sh"]

EXPOSE 8000
CMD ["run_all"]

RUN ${PROJECT_INSTALL_DIR}/bin/Saabaza_Web_App.py platformtemplate supervisord_docker > /etc/supervisor/conf.d/appsaabaza.conf \
&& apt-get clean autoclean \
&& apt-get autoremove --purge -y \
&& rm -rf /var/lib/apt/lists/* \
&& rm -f /var/cache/apt/archives/*.deb \
# Remove temporary files owned by root from the platformtemplate step
&& rm /tmp/* \
# Keep displaying log messages to stdout
&& find /var/log -type f | while read f; do echo -ne '' > $f; done;
