#!/bin/bash
#SBATCH --job-name=no_vort_source_but_vort_wall_sink_and_global_vort_sink
#SBATCH --mail-type=NONE
#SBATCH --partition=xeon24
#SBATCH -N 1 # Number of nodes
#SBATCH -n 24 # Total number of tasks
#SBATCH --time=0-2:10:00
#SBATCH --output=./slurm_out/north_%j_%x_ESEL.log
#SBATCH --error=./slurm_out/north_%j_%x_ESEL_err.log

# Set input and output directory
IN_DIR=$PWD/data
# NOTE: Change IN_DIR if using restart and append=true
# IN_DIR=$PWD/data_5703126

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

# mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true append=false wall_limit = 3
# NOTE: Change IN_DIR if using restart and append=true
# mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true restart append=true wall_limit = 24
# mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true restart append=true wall_limit=6 north:Dn=5e-3 north:DT=5e-3 north:Dvort=5e-3 north:tau_wall_scale=10

# NOTE: Use this to set flags for input parameters while running
mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true append=false wall_limit=2 north:Dn=5e-3 north:DT=5e-3 north:Dvort=5e-3 north:tau_wall_scale=10

# When done: Move output files back to output directory
mkdir -p $OUT_DIR
mv $SCRATCH_DIR/data/* $OUT_DIR

# Clear cache
rm -rf $SCRATCH_DIR/*