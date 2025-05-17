#!/bin/bash

#SBATCH --job-name=VDJ_Job
#SBATCH --time=72:00:00
#SBATCH --output=/work/s/st25/my_work/vdj-main/Output/out.RunVDJ.%A_%a
#SBATCH --error=/work/s/st25/my_work/vdj-main/Error/err.RunVDJ.%A_%a
#SBATCH --array=0-10
#SBATCH --mem=100250
#SBATCH --partition=rra
#SBATCH --qos=rra
#SBATCH --ntasks-per-node=20
#SBATCH --nodes=1

#SBATCH --mail-type=ALL
#SBATCH --mail-user=placeholder@aot.com

# need to change array=0-numjobs depending on console output from t3_set_task_items.py

module load apps/python/3.8.5
IFS='#' read -a receptors_to_do < /work/s/st25/my_work/vdj-main/t3_rectodo.txt
#receptors_to_do=(TRA TRB TRD TRG TRA_UM TRB_UM TRD_UM TRG_UM)


echo "array task id:" $SLURM_ARRAY_TASK_ID
echo "receptor:" ${receptors_to_do[$SLURM_ARRAY_TASK_ID]}
results_dir="/work/s/st25/my_work/vdj-main/BAMs_Results/"
vdjdb="/work/s/st25/my_work/vdj-main/t3_vdjdb/"
python3 -u "/work/s/st25/my_work/vdj-main/t3_findvdjum.py" ${receptors_to_do[$SLURM_ARRAY_TASK_ID]} $results_dir $vdjdb

echo 'done'
