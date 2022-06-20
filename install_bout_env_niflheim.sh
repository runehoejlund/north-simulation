#!/usr/bin/bash
# Install Bout++ Dependencies: HDF5, NetCDF on Niflheim

FORCE=true # Set to true to reconfigure and recompile all software modules (even though they're already installed)
START_DIR=$PWD
VENV_NAME=$1
VENV_DIR=~/local/venv/$VENV_NAME
USAGE="Usage: ./install_bout_env_niflheim.sh venv_name"

if [[ $# != 1 ]]; then
    echo "Wrong number of arguments, expected 1 got $#"
    echo $USAGE
    cd $START_DIR
    return
fi

MOD_DIR=~/local/modules
MOD_FILES_DIR=$MOD_DIR/modules/all
MOD_DOWN_DIR=$MOD_DIR/downloads
MOD_INSTALL_DIR=$MOD_DIR/software

echo "purging modules and loading tool-chains: foss, Python"
module purge
module load foss Python

echo "copying module files to $MOD_FILES_DIR"
mkdir -p $MOD_FILES_DIR
cp -r $PWD/modulefiles/* $MOD_FILES_DIR

mkdir -p $MOD_DOWN_DIR

# Install HDF5
echo "####################################"
if [[ (! -d $MOD_INSTALL_DIR/HDF5/1.12.1) || $FORCE ]]; then
    echo "Installing HDF5 at $MOD_INSTALL_DIR/HDF5/1.12.1"
    cd $MOD_DOWN_DIR
    if [ ! -d ./hdf5-1.12.1 ]; then
        wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.12/hdf5-1.12.1/src/hdf5-1.12.1.tar.gz
        tar -xzvf hdf5-1.12.1.tar.gz
    fi
    cd hdf5-1.12.1
    mkdir -p $MOD_INSTALL_DIR/HDF5/1.12.1
    ./configure --prefix=$MOD_INSTALL_DIR/HDF5/1.12.1
    make
    make install
else
    echo "HDF5 already installed. Skipping this step."
fi

# Use project module files and load modules
module use $MOD_FILES_DIR
module load HDF5/1.12.1

# Install NetCDF-C
echo "####################################"
if [[ (! -d $MOD_INSTALL_DIR/netCDF) || $FORCE ]]; then
    echo "Installing NetCDF-C"
    cd $MOD_DOWN_DIR
    if [ ! -d ./netcdf-c-4.8.1 ]; then
        wget https://downloads.unidata.ucar.edu/netcdf-c/4.8.1/netcdf-c-4.8.1.tar.gz
        tar -xzvf netcdf-c-4.8.1.tar.gz
    fi
    cd netcdf-c-4.8.1
    mkdir -p $MOD_INSTALL_DIR/netCDF
    ./configure --prefix=$MOD_INSTALL_DIR/netCDF
    make
    make install

    # load NetCDF-C before installing netCDF-C++
    module use $MOD_FILES_DIR
    module load netCDF/2022

    # Install NetCDF-C++ in same location as NetCDF-C
    echo "Installing NetCDF-C++"
    cd $MOD_DOWN_DIR
    if [ ! -d ./netcdf-cxx4-4.3.1 ]; then
        wget https://downloads.unidata.ucar.edu/netcdf-cxx/4.3.1/netcdf-cxx4-4.3.1.tar.gz
        tar -xzvf netcdf-cxx4-4.3.1.tar.gz
    fi
    cd netcdf-cxx4-4.3.1
    ./configure --prefix=$MOD_INSTALL_DIR/netCDF
    make
    make install
else
    echo "NetCDF already installed. Skipping this step."
fi

echo "####################################"
echo "Install and setup myqueue"
# Create venv:
echo "Creating virtual environment $VENV_NAME"
mkdir -p $VENV_DIR
python3 -m venv --system-site-packages $VENV_DIR
cd $VENV_DIR
. bin/activate
PIP="python3 -m pip"
$PIP install --upgrade pip -qq
$PIP install myqueue
mq completion >> bin/activate
$PIP completion --bash >> bin/activate
. bin/activate

# Purge and reload all required modules
module purge
module use $MOD_FILES_DIR
module load foss HDF5/1.12.1 netCDF/2022 Python
module save bout

# # Install Bout-Dev
# echo "####################################"
# echo "Installing Bout-Dev"
# cd ~/north-simulation/shared
# git clone https://github.com/boutproject/BOUT-dev.git
# cd BOUT-dev
# ./configure
# make

echo "####################################"
echo "Succesfully installed all requirements"
echo "Add the following to your .bashrc to make modules available "
echo "and activate python venv (you may use ~/ "
echo "instead of full user directory)."
echo ""
echo "module use $MOD_FILES_DIR"
echo ". $VENV_DIR/bin/activate"
echo "####################################"
echo "Use the following command to activate the environment:"
echo "module restore bout"
echo "####################################"

cd $START_DIR
