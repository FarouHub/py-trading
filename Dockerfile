FROM python:alpine3.17

RUN apk update
RUN apk add \
    build-base \
    freetds-dev \
    g++ \
    gcc \
    tar \
    gfortran \
    gnupg \
    libffi-dev \
    libpng-dev \
    libsasl \
    openblas-dev \
    openssl-dev 

# install dependencies
COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt


CMD ["python", "./main"]