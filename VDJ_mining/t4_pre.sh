#!/bin/bash
#SBATCH --job-name=t4convert
#SBATCH --time=72:00:00
#SBATCH --output=/work/s/st25/my_work/vdj-main/Output/out.t4pre.%A_%a
#SBATCH --mem=180250
#SBATCH --partition=rra
#SBATCH --qos=rra
#SBATCH --nodes=1
#SBATCH --mail-type=ALL
#SBATCH --mail-user=placeholder@aot.com

module load apps/python/3.8.5
python3 -m pip install openpyxl
python3 -u "/work/s/st25/my_work/vdj-main/t4_pre.py"