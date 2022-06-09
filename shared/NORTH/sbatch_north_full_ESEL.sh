#!/bin/bash
#SBATCH --mail-type=NONE
#SBATCH --partition=xeon16
#SBATCH -N 1 # Number of nodes
#SBATCH -n 16 # Total number of tasks
#SBATCH --time=1-00:15:00
#SBATCH --output=./slurm_out/north_full_ESEL.log
#SBATCH --error=./slurm_out/north_full_ESEL_err.log

module use ~/local/modules/modules/all
source ~/local/venv/north-simulation/bin/activate
module restore bout

./north_full_ESEL
