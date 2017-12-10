#!/bin/bash

#--------------------------------------------------------------------------------
# configuration
#--------------------------------------------------------------------------------
listFilepath=assembly.list
baseDirec=/work/GoryaninU/mitsuki/out/taxonomy/36m_anode

#--------------------------------------------------------------------------------
# distribute each scaffold
#--------------------------------------------------------------------------------
cmd=seq_distributer.sh
numJobs=1
jobId=`sbatch --parsable ${cmd} ${listFilepath} ${baseDirec}`
echo "submitted ${numJobs} jobs with job_id=${jobId}"

#--------------------------------------------------------------------------------
# annotate scaffolds
#--------------------------------------------------------------------------------
cmd=prodigal.sh
argCmd="./arg/${cmd/.sh/.py} ${listFilepath} ${baseDirec}"
argFilepath=./arg/${cmd/.sh/.list}
eval ${argCmd} > ${argFilepath}
numJobs=`grep -c '' ${argFilepath}`
prevJobId=${jobId}
jobId=`sbatch --parsable --array=1-${numJobs} --dependency=afterok:${prevJobId} ${cmd} ${argFilepath}`
echo "submitted ${numJobs} jobs with job_id=${jobId}, dependency=${prevJobId}"

#--------------------------------------------------------------------------------
# merge gene sequences into one
#--------------------------------------------------------------------------------
cmd=gene_merger.sh
numJobs=1
prevJobId=${jobId}
jobId=`sbatch --parsable --dependency=afterok:${prevJobId} ${cmd} ${listFilepath} ${baseDirec}`
echo "submitted ${numJobs} jobs with job_id=${jobId}, dependency=${prevJobId}"

#--------------------------------------------------------------------------------
# run mmseqs
#--------------------------------------------------------------------------------
cmd=mmseqs.sh
numJobs=1
prevJobId=${jobId}
jobId=`sbatch --parsable --dependency=afterok:${prevJobId} ${cmd} ${baseDirec}`
echo "submitted ${numJobs} jobs with job_id=${jobId}, dependency=${prevJobId}"

#--------------------------------------------------------------------------------
# add taxnomy information based on best similarity
#--------------------------------------------------------------------------------
cmd=taxonomy_assignment.sh
numJobs=1
prevJobId=${jobId}
jobId=`sbatch --parsable --dependency=afterok:${prevJobId} ${cmd} ${baseDirec}`
echo "submitted ${numJobs} jobs with job_id=${jobId}, dependency=${prevJobId}"
