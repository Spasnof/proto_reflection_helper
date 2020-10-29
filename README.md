Small docker image / python script to produce a case class of any arbitrary .proto. Useful if a proto is used as the definition of a schema in spark.
## Requirements 
- Docker
- (If providing own protos) a compilable proto.

## To run
1. Build the image via `docker build -t <tagname> .`
   - ie `docker build -t test .`
2. Run the image via `docker run <tagname>`
   - ie `docker run test`

    
## To run with your own protos
1. Mount the protos you want to the `\app\mounted_protos` container path.
2. set the `ENTRYPROTO` envar on the container to your .proto file you want to run.
    - Currently this does not support multiple .protos due to limitations/hacks on  how the `*_pb2.py` files are imported.
    
Example Powershell:
```shell script
docker run -e ENTRYPROTO=added.proto -v $PWD\example_protos\added.proto:/app/mounted_protos/added.proto test
```

