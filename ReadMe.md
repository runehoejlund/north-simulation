# North Simulation
Numerical model for a magnetically confined plasma in the NORTH tokamak. Note: The bout++ model was developed at DTU Physics by the Plasma Physics and Fusion Energy group. We use [BOUT++](http://boutproject.github.io/) for numerical simulation.

## Getting started

### Running Simulations with bout++ container
You need to have downloaded [Docker](https://docker.com/get-started) to run the project.

1. Open a terminal from the project folder and run the following commands

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