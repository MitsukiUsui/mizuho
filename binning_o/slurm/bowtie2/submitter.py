#!/usr/bin/env python3

from myutil.myutil import myrun

def main(numBins):
    for binId in range(1, numBins + 1):
        binDirec="/work/GoryaninU/mitsuki/out/binning/bin/bin{:03d}".format(binId)
        scaffFilepath="{}/scaffolds.fasta".format(binDirec)
        leftFilepath="{}/bin{:03d}_R1.fastq".format(binDirec, binId)
        rightFilepath="{}/bin{:03d}_R2.fastq".format(binDirec, binId)
        samFilepath="{}/best.sam".format(binDirec)
        cmd = "sbatch caller.sh {} {} {} {}".format(scaffFilepath, leftFilepath, rightFilepath, samFilepath)
        #print(cmd)
        myrun(cmd)
            
if __name__=="__main__":
    numBins=184
    main(numBins)
