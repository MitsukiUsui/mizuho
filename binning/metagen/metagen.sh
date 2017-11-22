#!/bin/bash

#SBATCH --job-name=metagen
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --output=./log/metagen.out
#SBATCH --err=./log/metagen.err
#SBATCH --mem=50g
#SBATCH --time=0-03 

metagen_work=/work/GoryaninU/mitsuki/out/binning/metagen
metagen_path=/home/m/mitsuki-usui/software/MetaGen
num_thread=8
bic_min=10
bic_max=300
bic_step=5
thred=0.05
ini_prop=1
min_ctg_len=500
bic_plot=F
bic_method=2

Rscript $metagen_path/R/metagen.R \
        -m $metagen_path -w $metagen_work \
        -n $num_thread \
        -i $bic_min -a $bic_max -s $bic_step \
        -t $thred -p $ini_prop -l $min_ctg_len -p $bic_plot -o $bic_method
