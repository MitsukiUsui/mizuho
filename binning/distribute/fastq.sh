#!/bin/bash

FORCE_MODE=false

#--------------------------------------------------------------------------------
# create index for all database
#--------------------------------------------------------------------------------
binningDirec=/work/GoryaninU/mitsuki/out/binning
scaffFilepath=${binningDirec}/metagen/contigs/Contigs.fasta
dbFilepath=${binningDirec}/distribute/bowtie/index/all
arg1=arg1.list
echo ${scaffFilepath},${dbFilepath} > ${arg1}
jobId1=`sbatch --parsable --array=1-1 ../metagen/index.sh ${arg1}`
echo "submitted 1 job with job_id="${jobId1}

#--------------------------------------------------------------------------------
# map reads
#--------------------------------------------------------------------------------
arg2=arg2.list
./arg/map.py > ${arg2}
numJobs2=`grep -c '' ${arg2}`
jobId2=`sbatch --parsable --array=1-${numJobs2} --dependency=afterok:${jobId1} ../metagen/map.sh ${arg2}`
echo "submitted "${numJobs2}" jobs with job_id="${jobId2}", dependency="${jobId1}

#--------------------------------------------------------------------------------
# distribute fastq
#--------------------------------------------------------------------------------
arg3=arg3.list
./arg/distributefastq.py > ${arg3}
numJobs3=`grep -c '' ${arg3}`
jobId3=`sbatch --parsable --array=1-${numJobs3} --dependency=afterok:${jobId2} distributefastq.sh ${arg3}`
echo "submitted "${numJobs3}" jobs with job_id="${jobId3}", dependency="${jobId2}

#--------------------------------------------------------------------------------
# merge fastq
#--------------------------------------------------------------------------------
numBins=173
numJobs4=${numBins}
jobId4=`sbatch --parsable --array=1-${numJobs4} --dependency=afterok:${jobId3} mergefastq.sh`
echo "submitted "${numJobs4}" jobs with job_id="${jobId4}", dependency="${jobId3}
