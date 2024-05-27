# podman run -it --rm -it --device nvidia.com/gpu=all --security-opt=label=disable --shm-size=20GB localhost/ccmnet:base
FROM nvcr.io/nvidia/jax:23.10-py3

LABEL Maintainer="Martin Proks <martin.proks@sund.ku.dk>"

RUN apt update && \
    apt install -y time && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists

RUN pip install --no-cache-dir git+https://github.com/brickmanlab/ccmnet.git@dev

RUN mkdir data/
