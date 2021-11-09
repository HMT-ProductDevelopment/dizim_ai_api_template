# Build a docker that run the service
# author: Xuan-Son Vu
# 26 Aug 2021

# base image
ARG DEBIAN_FRONTEND=noninteractive
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# set the working directory
WORKDIR .
COPY requirements.txt ./

RUN apt update && apt-get install -y apt-utils 2>&1 && apt install ffmpeg libsndfile1 --yes --no-install-recommends && \
    pip install --upgrade pip && pip install -r requirements.txt

COPY ./ .

# start serving
CMD python3 serve.py
