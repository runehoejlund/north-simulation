# North Simulation
Numerical reduced fluid model of perpendicular dynamics a magnetically confined plasma in the NORTH tokamak. We use [BOUT++](http://boutproject.github.io/) for numerical simulation. Note: The bout++ model is an implementation of the ESEL equations, developed at DTU Physics by the Plasma Physics and Fusion Energy group.

The results can be seen in the folder [presentation of main results](https://github.com/PPFE-Turbulence/north-simulation/tree/master/presentation%20of%20main%20results).

To reproduce the main results of the data analysis, open and run the iPython Notebook `main_results.ipynb`. Note: It requires data from a simulation run. See the documentaion below on how to run simulations either on the Niflheim environment or (perhaps easier for a start) on your personal computer.

## Getting started
---------------------------------------------------------
### Niflheim (HPC-environment): First time Setup:
Skim the Niflheim user guide: https://wiki.fysik.dtu.dk/niflheim/Niflheim7_Getting_started.
I used the slid-node.
1. Clone the git repository to Niflheim and open the repository directory:
```
git clone https://github.com/runehoejlund/north-simulation.git
cd ./north-simulation
```
2. Install necessary dependencies. We need to build our own modules for HDF5, netCDF-C and netCDF-C++. Niflheim uses [Lmod](https://lmod.readthedocs.io/en/latest/) for handling software modules. The installation script should take care of everything:
```
. ./install_bout_env_niflheim.sh north-simulation
```
3. Install python-requirements to the python venv with pip:
```
. ~/local/venv/north-simulation/bin/activate
pip install -r requirements.txt
```
4. Navigate to the shared directory and clone and compile the Bout-dev git (make sure the path `~/north-simulation` equals the path to the repo directory):
```
module restore bout
cd ~/north-simulation/shared
git clone https://github.com/boutproject/BOUT-dev.git
cd BOUT-dev
./configure
make
```

### Niflheim (HPC-environment): Running simulations
Use `module restore bout` to load in module collection (which was saved in previous step). You may add this line to the file `.bashrc`, which is located at your user directory (`cd ~/`), in order to automatically load required modules on every login.
1. Navigate to the simulation code directory
```
cd shared/NORTH/
```
2. Compile simulation code
```
make
```
3. Start simulations
``` 
./north_full_ESEL
```
**NOTE:** The command above starts simulations directly on the node, which is not recommended (but it's useful for verifying that the code will evens start running). Instead you should queue the simulations using slurm:

### Niflheim: Slurm Commands
I've included the script `./shared/NORTH/sbatch_north_full_ESEL.sh` which takes care of queuing simulations using SLURM. Here is how to do it:
- Before running the sbatch script: Navigate to `shared/NORTH/`. In there, create a directory for output logs:
```
mkdir slurm_out
```
- Submit batch job (look at Slurm Batch job script in `shared/NORTH/` for how to write a sbatch file):
```
sbatch sbatch_north_full_ESEL.sh
```
- show your queue
```
squeue -u $USER
```
- Cancel all your jobs:
```
scancel -u $USER
```
- Cancel all pending jobs:
```
scancel -t PD
```
- Stop job gracefully (run file with `stopCheck=true` as is done in the slurm sbatch script), then add `BOUT.stop` file:
```
touch ./data/BOUT.stop
```

### Niflheim/VSCode: Trouble-Shooting
**bash: fork: retry: No child processes**

If VSCode causes a [fork bomb](https://stackoverflow.com/questions/47143093/linux-ssh-bash-fork-retry-no-child-processes) with the error message: `bash: fork: retry: No child processes`, simply open up a terminal and write
```
kill -9 -1
```

**Python Interpreter Problems**

If the VSCode Python Extension won't recognize your Python Interpreter. Pressing cmd/ctrl + shift P with the following command names are useful:
- `Python: Create Terminal`
- `Python: Run Python File in Terminal`
- `Python: Select Interpreter` > Enter Interpreter Path (e.g. `~/local/venv/north-simulation/bin/python`). If this doesn't work:
- `Python: Clear Workspace Interpreter Settings`

Alternatively, try downgrading the Python Extension by going to Extensions > Python (SSH - Installed, not Local - Installed) > click the down arrow next to the uninstall button and choose "Install another version" > 2022.18.2

---------------------------------------------------------
### Personal Computer: First time setup
Clone the repository to your computer. That is: Install git and navigate to the folder where you wish to work from and run the following command in terminal (powershell if using Windows).
```
git clone https://github.com/runehoejlund/north-simulation.git
```

### Personal computer: Set up (build and run) bout++ container
You need to have downloaded [Docker](https://docker.com/get-started) to run the project. Start Docker (so that the Docker Deamon is running). Open a terminal (Powershell if using Windows) from the project folder and run the following commands. **Note:** It's important that you are in the repository (project) folder. For example open the folder from VSCode.

1. Build docker image from the Dockerfile

```
docker build -t north-simulation .
```

2. Run the docker container using the just-built image with options:

`-it`: creates an interactive terminal in the container.
`-v`: creates shared directory. Files in the docker image put in `/home/boutuser/bout-img-shared` should be visible in your host `shared` directory.

```
docker run -it --name north-container -v $PWD/shared:/home/boutuser/bout-img-shared north-simulation
```

3. **Note:** Currently the simulation only works with the BOUT-dev framework, and therefore we actually don't use the bout-distribution from the Docker image above. Therefore, currently you should also navigate to the shared directory and clone and compile the Bout-dev git:
```
cd ./bout-img-shared
git clone git://github.com/boutproject/BOUT-dev.git
cd BOUT-dev
./configure
make
```

You might need to give sudo privileges to the boutuser on the docker container. You can do this by:
1. From your **host machine** (for example from VSCode on your personal computer), open up a new terminal/Powershell and run a *new* container as root user:

```
docker run -u 0 -it -v $PWD/shared:/home/boutuser/bout-img-shared north-simulation
```
2. Now, you're logged in as a root user, add the boutuser to the sudo group:

```
usermod -aG sudo boutuser
```

3. Kill the container
```
exit
```

### Personal Computer: Run Simulations
If the Docker container isn't already running, open up a terminal and start it up:
```
docker run -it -v $PWD/shared:/home/boutuser/bout-img-shared north-simulation
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
./north_full_ESEL
```

----------------------------------------------------
## Personal computer: Analysing simulated data with python
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

To reproduce the main results of the data analysis, refer to the iPython Notebook `main_results.ipynb`.

## Usefull commands
here are some usefull commands. If you're on your personal computer, I assume you have Docker running, started a Docker container and navigated to the north directory.

### Bout++ Commands
- Restart Simulation from where you left of, while **overwriting** output data BOUT.dmp.*.nc file.
```
./north_full_ESEL restart
```
- Restart Simulation from where you left of, while **keeping** previous output data BOUT.dmp.*.nc file.
```
./north_full_ESEL restart append
```
- Help on command line options
```
./north_full_ESEL -h
```