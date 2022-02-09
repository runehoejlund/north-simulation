# North Simulation
These are my personal notes for running the NORTH-simulation.
We use BOUT++ for numerical simulation of the plasma electron density in the North Tokamak.

## Getting started
You need [Docker](https://docker.com/get-started) to run the project.

1. Open a terminal from the current project folder and run the following commands
2. Create a shared directory on your "host" machine:

`mkdir shared`

2. Build docker image from the Dockerfile)

`docker build -t north-simulation .`

3. Run the docker container using the just-built image with options:

`-it`: creates an interactive terminal in the container.
`-v`: creates shared directory. Files in the docker image put in `/home/boutuser/bout-img-shared` should be visible in your host `shared` directory.

```
docker run -it \
   -v $PWD/shared:/home/boutuser/bout-img-shared \
   north-simulation
```

