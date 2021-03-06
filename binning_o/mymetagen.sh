#!/bin/bash

#SBATCH --job-name=metagen
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --input=none
#SBATCH --output=./log/metagen_%j.out
#SBATCH --error=./log/metagen_%j.err
#SBATCH --mem=100g
#SBATCH --time=0-04 

metagen_work=/work/GoryaninU/mitsuki/out/binning/metagen/all
metagen_path=/home/m/mitsuki-usui/software/MetaGen
num_thread=8
bic_min=10
bic_max=200
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
