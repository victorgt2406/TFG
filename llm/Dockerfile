FROM nvidia/cuda:12.3.2-runtime-ubuntu22.04

# Environment
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Madrid

ARG PYTHON_VERSION=3.11
ENV PYTHON_VERSION=${PYTHON_VERSION}

# Instalar las dependencias necesarias
RUN apt-get update && apt-get install -y \
    curl \
    locales \
    git \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    && apt-get clean

# Configurar la configuración regional
RUN locale-gen en_US.UTF-8

# librerias nvidia
RUN apt update
RUN apt install -y zlib1g libcudnn8 libcudnn8-dev

# pyenv
RUN git clone https://github.com/pyenv/pyenv.git root/.pyenv
RUN cd root/.pyenv && src/configure && make -C src

RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> root/.profile \
&& echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> root/.profile \
&& echo 'eval "$(pyenv init -)"' >> root/.profile

ENV PYENV_ROOT "/root/.pyenv"
ENV PATH "$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

# global python version
RUN pyenv install $PYTHON_VERSION && pyenv global $PYTHON_VERSION

COPY ./requirements.txt /cp-files/requirements.txt

RUN pip install -r /cp-files/requirements.txt
