#!/bin/bash
#SBATCH --mail-type=NONE
#SBATCH --partition=xeon16
#SBATCH -N 1 # Number of nodes
#SBATCH -n 1 # Total number of tasks
#SBATCH --time=0-00:00:10
#SBATCH --output=./slurm_out/north_full_$SLURM_NTASKS_%j_ESEL.log
#SBATCH --error=./slurm_out/north_full_$SLURM_NTASKS_%j_ESEL_err.log

echo %DATE

# module use ~/local/modules/modules/all
# module restore bout

# make
# mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true