#!/bin/bash

#--------------------------------------------------------------------------------
# create index
#--------------------------------------------------------------------------------
#cmd=index.sh
#argCmd=./arg/${cmd/.sh/.py}
#argFilepath=./arg/${cmd/.sh/.list}
#eval ${argCmd} > ${argFilepath}
#numJobs=`grep -c '' ${argFilepath}`
#jobId=`sbatch --parsable --array=1-${numJobs} ${cmd} ${argFilepath}`
#echo "submitted ${numJobs} jobs with job_id=${jobId}"

#--------------------------------------------------------------------------------
# map to the index created abobe
#--------------------------------------------------------------------------------
cmd=map.sh
argCmd=./arg/${cmd/.sh/.py}
argFilepath=./arg/${cmd/.sh/.list}
eval ${argCmd} > ${argFilepath}
numJobs=`grep -c '' ${argFilepath}`
#prevJobId=${jobId}
#jobId=`sbatch --parsable --array=1-${numJobs} --dependency=afterok:${prevJobId} ${cmd} ${argFilepath}`
jobId=`sbatch --parsable --array=1-${numJobs} ${cmd} ${argFilepath}`
echo "submitted ${numJobs} jobs with job_id=${jobId}, dependency=${prevJobId}"
