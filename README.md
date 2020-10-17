Helper script to size (roughtly) a proto 
## Requirements 
- protoc 2.6 (executible in path)
- protobuf 3.8 (pip library)
- bash generate_proto run.

## TODO
- [ ] put this inside a docker container.
- [ ] have the protoc and reflection all happen at runtime inside the container.
- [ ] test it in the wild on a few "real" protos
- [ ] (optional?) figure out what happened with the original `reflection_test.py` Did I just leave it broken?