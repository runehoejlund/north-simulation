#!/bin/bash
#SBATCH --job-name=new_diff
#SBATCH --mail-type=NONE
#SBATCH --partition=xeon24
#SBATCH -N 1 # Number of nodes
#SBATCH -n 24 # Total number of tasks
#SBATCH --time=0-09:10:00
#SBATCH --output=./slurm_out/north_full_%j_ESEL.log
#SBATCH --error=./slurm_out/north_full_%j_ESEL_err.log

# Set input and output directory
IN_DIR=$PWD/data
# NOTE: Change IN_DIR if using restart and append=true
# IN_DIR=$PWD/data_5674003

OUT_DIR=$PWD/data_$SLURM_JOB_ID
SCRATCH_DIR=/scratch/$USER/$SLURM_JOB_ID

# Load in modules
module purge
module use ~/local/modules/modules/all
module restore bout

# # Reconfigure Bout-Dev
# cd ../BOUT-dev/
# ./configure
# make
# cd ../NORTH/

# Copy all necessary files to scratch folder
mkdir -p $SCRATCH_DIR
cp $IN_DIR $SCRATCH_DIR/data -r
cp ./BoutFastOutput $SCRATCH_DIR/BoutFastOutput -r
cp ./dependencies $SCRATCH_DIR/dependencies -r
cp north_full_ESEL.cxx $SCRATCH_DIR
cp makefile $SCRATCH_DIR
cd $SCRATCH_DIR

# Compile and run
make

mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true append=false wall_limit = 9
# NOTE: Change IN_DIR if using restart and append=true
# mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true restart append=true wall_limit = 24
# NOTE: Use this to set flags for input parameters while running
# mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true append=false wall_limit = 1 north:k_ei=0

# When done: Move output files back to output directory
mkdir -p $OUT_DIR
mv $SCRATCH_DIR/data/* $OUT_DIR

# Clear cache
rm -rf $SCRATCH_DIR/*