#!/bin/bash

cmd=divide.sh
argFilepath=sample.list
numJobs=`grep -c '' ${argFilepath}`
jobId=`sbatch --parsable --array=1-${numJobs} ${cmd} ${argFilepath}`
echo "submitted ${numJobs} jobs with job_id=${jobId}"

cmd=merge.sh
prevArgFilepath=${argFilepath}
argCmd=./arg/${cmd/.sh/.py}
argFilepath=./arg/${cmd/.sh/.list}
eval ${argCmd} > ${argFilepath}
numJobs=`grep -c '' ${argFilepath}`
prevJobId=${jobId}
jobId=`sbatch --parsable --array=1-${numJobs} --dependency=afterok:${prevJobId} ${cmd} ${argFilepath} ${prevArgFilepath}`
echo "submitted ${numJobs} jobs with job_id=${jobId}, dependency=${prevJobId}"
