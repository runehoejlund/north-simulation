# North Simulation
Numerical model for a magnetically confined plasma in the NORTH tokamak. Note: The bout++ model was developed at DTU Physics by the Plasma Physics and Fusion Energy group. We use [BOUT++](http://boutproject.github.io/) for numerical simulation.

## Getting started

### Setting up (build and run) bout++ container
You need to have downloaded [Docker](https://docker.com/get-started) to run the project. Start Docker (so that the Docker Deamon is running). Open a terminal from the project folder and run the following commands

1. Build docker image from the Dockerfile

```
docker build -t north-simulation .
```

2. Run the docker container using the just-built image with options:

`-it`: creates an interactive terminal in the container.
`-v`: creates shared directory. Files in the docker image put in `/home/boutuser/bout-img-shared` should be visible in your host `shared` directory.

```
docker run -it \
   -v $PWD/shared:/home/boutuser/bout-img-shared \
   north-simulation
```

3. **Note:** Currently the simulation only works with the BOUT-dev framework, and therefore we actually don't use the bout-distribution from the Docker image above. Therefore, currently you should also navigate to the shared directory and clone and compile the Bout-dev git:
```
cd ./bout-img-shared
git clone git://github.com/boutproject/BOUT-dev.git
cd BOUT-dev
./configure
make
```

### Run Simulations
If the Docker container isn't already running, open up a terminal and start it up:
```
docker run -it \
   -v $PWD/shared:/home/boutuser/bout-img-shared \
   north-simulation
```
From within the Docker container terminal run the following commands:
1. Navigate to the simulation code directory
```
cd bout-img-shared/NORTH/
```
2. Compile simulation code
```
make
```
3. Start simulations
``` 
./north
```

### Analysing simulated data with python
The project is setup to analyse the data and plot the results on the host environment (i.e. on you personal computer and not in the docker container). You need a python installation (e.g. the Anaconda distribution) and an IDE for opening Jupyter Notebooks. I recommend creating a conda environment to ensure, that we're using the same python version and have the same requirements installed. Run the following commands from a terminal within the project directory:
1. Create a new environment (only first time)
```
conda create -n north-simulation python=3.7.6
```
2. Activate the environment:
```
conda activate north-simulation
```
3. Install all requirements
```
pip install -r requirements.txt
```

Run the file `data_analysis.py` to reproduce the main results.