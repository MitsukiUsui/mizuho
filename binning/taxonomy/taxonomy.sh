#!/bin/bash

cd /home/m/mitsuki-usui/mizuho/assembly/qa/taxonomy

#--------------------------------------------------------------------------------
# configuration
#--------------------------------------------------------------------------------
baseDirec=/work/GoryaninU/mitsuki/out/taxonomy/bin

#--------------------------------------------------------------------------------
# run mmseqs
#--------------------------------------------------------------------------------
cmd=mmseqs.sh
numJobs=1
jobId=`sbatch --parsable ${cmd} ${baseDirec}`
echo "submitted ${numJobs} jobs with job_id=${jobId}"

#--------------------------------------------------------------------------------
# add taxnomy information based on best similarity
#--------------------------------------------------------------------------------
cmd=taxonomy_assignment.sh
numJobs=1
prevJobId=${jobId}
jobId=`sbatch --parsable --dependency=afterok:${prevJobId} ${cmd} ${baseDirec}`
echo "submitted ${numJobs} jobs with job_id=${jobId}, dependency=${prevJobId}"
