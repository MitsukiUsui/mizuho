#!/bin/bash

#--------------------------------------------------------------------------------
# create bowtie index for each scaffolds
#--------------------------------------------------------------------------------
arg1=arg1.list
./arg/index.py > ${arg1}
numJobs1=`grep -c '' ${arg1}`
jobId1=`sbatch --parsable --array=1-${numJobs1} index.sh ${arg1}`
echo "submitted "${numJobs1}" jobs with job_id="${jobId1}

#--------------------------------------------------------------------------------
# map ehach samples for each scaffolds
#--------------------------------------------------------------------------------
arg2=arg2.list
./arg/map.py > ${arg2}
numJobs2=`grep -c '' ${arg2}`
jobId2=`sbatch --parsable --array=1-${numJobs2} --dependency=afterok:${jobId1} map.sh ${arg2}`
echo "submitted "${numJobs2}" jobs with job_id="${jobId2}", dependency="${jobId1}

#--------------------------------------------------------------------------------
# summarize information for metagen
#--------------------------------------------------------------------------------
jobId3=`sbatch --parsable --dependency=afterok:${jobId2} prepare.sh`
echo "submitted with job_id="${jobId3}", dependency="${jobId2}

#--------------------------------------------------------------------------------
# main
#--------------------------------------------------------------------------------
jobId4=`sbatch --parsable --dependency=afterok:${jobId3} metagen.sh`
echo "submitted with job_id="${jobId4}", dependency="${jobId3}
