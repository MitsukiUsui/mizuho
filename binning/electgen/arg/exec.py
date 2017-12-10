#!/usr/bin/env python3

dbFilepath="/home/m/mitsuki-usui/mizuho/read/electgen/electgen"
numCluster=44
for clusterNum in range(1, numCluster+1):
    baseDirec="/work/GoryaninU/mitsuki/out/checkm/mycc/out/bins/Cluster.{}".format(clusterNum)
    queryFilepath="{}/genes.faa".format(baseDirec)
    outFilepath="{}/electgen.m8".format(baseDirec)
    print("{},{},{}".format(dbFilepath, queryFilepath, outFilepath))
