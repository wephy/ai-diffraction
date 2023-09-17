#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=42
#SBATCH --mem-per-cpu=3850
#SBATCH --partition=compute
#SBATCH --time=30:00:00

module restore felix-ml

srun python src/train.py --dataroot ~/FDP --split ./data/splits/1 --gpu_ids -1

