#!/usr/bin/bash
# Install Bout++ Dependencies: HDF5, NetCDF on Niflheim

START_DIR=$PWD

MOD_DIR=~/local/modules
MOD_FILES_DIR=$MOD_DIR/modules/all
MOD_DOWN_DIR=$MOD_DIR/downloads
MOD_INSTALL_DIR=$MOD_DIR/software

echo "purging modules and loading tool-chains: foss, intel"
module purge
module load foss intel

echo "copying module files to $MOD_FILES_DIR"
mkdir -p $MOD_FILES_DIR
cp -r $PWD/modulefiles/* $MOD_FILES_DIR

mkdir -p $MOD_DOWN_DIR

# Install HDF5
echo "####################################"
if [ ! -d $MOD_INSTALL_DIR/HDF5/1.12.1 ]; then
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
if [ ! -d $MOD_INSTALL_DIR/netCDF ]; then
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

# Purge and reload all required modules
module purge
module use $MOD_FILES_DIR
module load foss intel HDF5/1.12.1 netCDF/2022
module save bout

echo "####################################"
echo "Succesfully installed all requirements"
echo "Add the following to your .bashrc to make modules available"
echo "module use $MOD_FILES_DIR"
echo "####################################"
echo "Use the following command to activate the environment:"
echo "module restore bout"
echo "####################################"

cd $START_DIR