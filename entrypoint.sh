#!/bin/bash
#if we mount any protos from the host enviroment copy them within the container.
cp -r /app/mounted_protos/* /app/protos
#HACK rename the proto we are starting with to make the python import happy
mv /app/protos/$ENTRYPROTO /app/protos/entrypoint.proto

#compile the protos
cd /app/protos
protoc --python_out=. *.proto
export PYTHONPATH="${PYTHONPATH}:/app/protos"

#generate the case classes
python3 /app/generate_scala_caseclass.py
