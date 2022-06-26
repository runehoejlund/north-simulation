#!/bin/bash
#SBATCH --mail-type=NONE
#SBATCH --partition=xeon40
#SBATCH -N 1 # Number of nodes
#SBATCH -n 40 # Total number of tasks
#SBATCH --time=0-01:05:00
#SBATCH --output=./slurm_out/north_full_%j_ESEL.log
#SBATCH --error=./slurm_out/north_full_%j_ESEL_err.log

# Set input and output directory
IN_DIR=$PWD/data
OUT_DIR=$PWD/data_$SLURM_JOB_ID
mkdir -p $OUT_DIR

# Load in modules
module use ~/local/modules/modules/all
module restore bout

# Copy all necessary files to scratch folder
cp $IN_DIR /scratch/$USER/data -r
cp ./BoutFastOutput /scratch/$USER/BoutFastOutput -r
cp ./dependencies /scratch/$USER/dependencies -r
cp north_full_ESEL.cxx /scratch/$USER
cp makefile /scratch/$USER
cd /scratch/$USER

# Compile and run
make
mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true append=false wall_limit = 1
# NOTE: Change IN_DIR if using restart and append=true
# mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true restart append=true wall_limit = 1
# NOTE: Use this to set flags for input parameters while running
# mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true append=false laplace:flags=0

# When done: Move output files back to output directory
mv /scratch/$USER/data/* $OUT_DIR

# Clear cache
rm -rf /scratch/$USER/*