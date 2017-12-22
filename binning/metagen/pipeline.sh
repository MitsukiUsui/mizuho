#!/bin/bash

#--------------------------------------------------------------------------------
# configuration
#--------------------------------------------------------------------------------
baseDirec=/work/GoryaninU/mitsuki/out/metagen/MFC1_36m_anode

#--------------------------------------------------------------------------------
# create bowtie index for each scaffolds
#--------------------------------------------------------------------------------
cmd=index.sh
argCmd="./arg/${cmd/.sh/.py} ${baseDirec}"
argFilepath=./arg/${cmd/.sh/.list}
eval ${argCmd} > ${argFilepath}
numJobs=`grep -c '' ${argFilepath}`
jobId=`sbatch --parsable --array=1-${numJobs} ${cmd} ${argFilepath}`
echo "submitted ${numJobs} jobs with job_id=${jobId}"

#--------------------------------------------------------------------------------
# map ehach samples for each scaffolds
#--------------------------------------------------------------------------------
cmd=map.sh
argCmd="./arg/${cmd/.sh/.py} ${baseDirec}"
argFilepath=./arg/${cmd/.sh/.list}
eval ${argCmd} > ${argFilepath}
numJobs=`grep -c '' ${argFilepath}`
prevJobId=${jobId}
jobId=`sbatch --parsable --array=1-${numJobs} --dependency=afterok:${prevJobId} ${cmd} ${argFilepath}`
echo "submitted ${numJobs} jobs with job_id=${jobId}, dependency=${prevJobId}"

#--------------------------------------------------------------------------------
# summarize information for metagen
#--------------------------------------------------------------------------------
cmd=prepare.sh
numJobs=1
prevJobId=${jobId}
jobId=`sbatch --parsable --dependency=afterok:${prevJobId} ${cmd} ${baseDirec}`
echo "submitted ${numJobs} jobs with job_id=${jobId}, dependency=${prevJobId}"
#
##--------------------------------------------------------------------------------
## main
##--------------------------------------------------------------------------------
cmd=metagen.sh
numJobs=1
prevJobId=${jobId}
jobId=`sbatch --parsable --dependency=afterok:${prevJobId} ${cmd} ${baseDirec}`
echo "submitted ${numJobs} jobs with job_id=${jobId}, dependency=${prevJobId}"
