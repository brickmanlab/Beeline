FROM mambaorg/micromamba:1.5-mantic

LABEL Maintainer="Aditya Pratapa <adyprat@vt.edu>"

USER root

RUN apt-get update && apt-get install -y time && \
    rm -rf /var/lib/apt/lists/*

RUN micromamba install --yes --name base -c bioconda -c conda-forge \
    arboreto==0.1.6
RUN micromamba clean --all --yes

#ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY runArboreto.py /

RUN mkdir data/