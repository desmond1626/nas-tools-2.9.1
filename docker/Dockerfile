FROM mcr.microsoft.com/playwright/python:v1.31.0-focal
RUN apt-get update \
    && apt-get -y install libffi-dev wget cron \
    && apt-get -y install $(echo $(wget --no-check-certificate -qO- https://raw.githubusercontent.com/desmond1626/nas-tools-2.9.1/master/package_list.txt)) \
    && ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo "${TZ}" > /etc/timezone \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && curl https://rclone.org/install.sh | bash \
    && if [ "$(uname -m)" = "x86_64" ]; then ARCH=amd64; elif [ "$(uname -m)" = "aarch64" ]; then ARCH=arm64; fi \
    && curl https://dl.min.io/client/mc/release/linux-${ARCH}/mc --create-dirs -o /usr/bin/mc \
    && chmod +x /usr/bin/mc \
    && pip install --upgrade pip setuptools wheel \
    && pip install cython \
    && pip install -r https://raw.githubusercontent.com/desmond1626/nas-tools-2.9.1/master/requirements.txt \
    && apt-get --purge -y remove libffi-dev \
    && playwright install chromium --with-deps  \
    && rm -rf /tmp/* /root/.cache/* /var/cache/apt/*
ENV LANG="C.UTF-8" \
    TZ="Asia/Shanghai" \
    NASTOOL_CONFIG="/config/config.yaml" \
    NASTOOL_AUTO_UPDATE=true \
    NASTOOL_CN_UPDATE=true \
    NASTOOL_VERSION=master \
    PS1="\u@\h:\w \$ " \
    REPO_URL="https://github.com/desmond1626/nas-tools-2.9.1.git" \
    PYPI_MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple" \
    ALPINE_MIRROR="mirrors.ustc.edu.cn" \
    PUID=0 \
    PGID=0 \
    UMASK=000 \
    WORKDIR="/nas-tools"
WORKDIR ${WORKDIR}
RUN python_ver=$(python3 -V | awk '{print $2}') \
    && echo "${WORKDIR}/" > /usr/local/lib/python${python_ver%.*}/dist-packages/nas-tools.pth \
    && echo 'fs.inotify.max_user_watches=524288' >> /etc/sysctl.conf \
    && echo 'fs.inotify.max_user_instances=524288' >> /etc/sysctl.conf \
    && git config --global pull.ff only \
    && git clone -b master ${REPO_URL} ${WORKDIR} --depth=1 --recurse-submodule \
    && git config --global --add safe.directory ${WORKDIR} \
    && apt-get -y install "${WORKDIR}/docker/chromedriver/google-chrome-stable_111.0.5563.64_amd64.deb" \
    && ln -s "${WORKDIR}/docker/chromedriver/chromedriver" /opt/google/chrome/chromedriver \
    && chmod 777 /nas-tools/docker/entrypoint.sh \
    && ln -s /ms-playwright /root/.cache/
EXPOSE 3000
VOLUME ["/config"]
ENTRYPOINT ["sh", "/nas-tools/docker/entrypoint.sh"]