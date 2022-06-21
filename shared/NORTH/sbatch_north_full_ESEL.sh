#!/bin/bash
#SBATCH --mail-type=NONE
#SBATCH --partition=xeon40
#SBATCH -N 1 # Number of nodes
#SBATCH -n 32 # Total number of tasks
#SBATCH --time=0-01:00:00
#SBATCH --output=./slurm_out/north_full_%j_ESEL.log
#SBATCH --error=./slurm_out/north_full_%j_ESEL_err.log

module use ~/local/modules/modules/all
module restore bout

make
mpirun -n $SLURM_NTASKS ./north_full_ESEL stopCheck=true
