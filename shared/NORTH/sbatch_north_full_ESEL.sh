#!/bin/bash
#SBATCH --mail-type=NONE
#SBATCH --partition=xeon40
#SBATCH -N 1 # Number of nodes
#SBATCH -n 40 # Total number of tasks
#SBATCH --time=0-02:00:00
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
echo "scratch dir content before cd"
echo $(ls /scratch/$USER/ -a)
cd /scratch/$USER

echo "scratch dir content after cd"
echo $(ls ./ -a)

# Compile and run
make
# NOTE: Change IN_DIR if using restart and append=true
mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true append=false

# When done: Move output files back to output directory
mv /scratch/$USER/data/* $OUT_DIR

# Clear cache
rm -rf /scratch/$USER/*