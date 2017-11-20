### exec
1. create list file for target scaffold, each line consist of ${assemblyName},${scaffoldFilepath}.
1. `./seq_distribute.py ${listFilepath} ${baseDirec}`
1. `./prodigal_submitter.sh ${listFilepath} ${baseDirec}`
1. (wait untill all prodigal jobs have finished)
1. `./gene_merger.py ${listFilepath} ${baseDirec}`
1. `sbatch mmseqs.sh ${baseDirec}`
1. `./taxonomy_assignment_gene.py ${baseDirec}`
1. `./taxonomy_assignment_scaffold.py ${baseDirec}`

