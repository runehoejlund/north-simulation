#!/bin/bash
#SBATCH --mail-type=NONE
#SBATCH --partition=xeon24
#SBATCH -N 1 # Number of nodes
#SBATCH -n 8 # Total number of tasks
#SBATCH --time=0-06:00:00
#SBATCH --output=./slurm_out/north_full_ESEL_2.log
#SBATCH --error=./slurm_out/north_full_ESEL_2_err.log

module use ~/local/modules/modules/all
module restore bout

make
mpirun -n $SLURM_NTASKS ./north_full_ESEL