# Docker

## Building it
docker build -t [tagname] .
docker run -p 8002:8000 [tagname]

## Pushing somewhere 
docker tag [tagname] [registryurl]/[tagname]
docker push [registryurl]/[tagname]