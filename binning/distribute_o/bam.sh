#!/bin/bash

#--------------------------------------------------------------------------------
# merge bams and distribute as sams
#--------------------------------------------------------------------------------
arg1=arg1.list
./arg/bamdistribute.py > ${arg1}
numJobs1=`grep -c '' ${arg1}`
jobId1=`sbatch --parsable --array=1-${numJobs1} bamdistribute.sh ${arg1}`
echo "submitted "${numJobs1}" jobs with job_id="${jobId1}

#--------------------------------------------------------------------------------
# merge sams into bam
#--------------------------------------------------------------------------------
arg2=arg2.list
./arg/mergesam.py > ${arg2}
numJobs2=`grep -c '' ${arg2}`
jobId2=`sbatch --parsable --array=1-${numJobs2} --dependency=afterok:${jobId1} mergesam.sh ${arg2}`
echo "submitted "${numJobs2}" jobs with job_id="${jobId2}", dependency="${jobId1}
