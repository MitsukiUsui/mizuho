#!/bin/bash

#--------------------------------------------------------------------------------
# create index
#--------------------------------------------------------------------------------
cmd=create_db.sh
argCmd=./arg/${cmd/.sh/.py}
argFilepath=./arg/${cmd/.sh/.list}
eval ${argCmd} > ${argFilepath}
numJobs=`grep -c '' ${argFilepath}`
jobId=`sbatch --parsable --array=1-${numJobs} ${cmd} ${argFilepath}`
echo "submitted ${numJobs} jobs with job_id=${jobId}"
