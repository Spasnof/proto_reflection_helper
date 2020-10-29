FROM python:3.9.0-slim-buster

RUN pip3 install protobuf
RUN apt-get update
RUN apt-get install -y protobuf-compiler

RUN mkdir /app
RUN mkdir /app/mounted_protos
COPY app/ /app
COPY entrypoint.sh /entrypoint.sh

WORKDIR /app/protos


#RUN protoc --python_out=. *.proto
#RUN python3 /app/generate_scala_caseclass.py
ENV ENTRYPROTO example.proto

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]



