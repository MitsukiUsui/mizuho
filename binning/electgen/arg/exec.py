#!/usr/bin/env python3

dbFilepath="/home/m/mitsuki-usui/mizuho/read/electgen/transfer"
numCluster=67
for clusterNum in range(1, numCluster+1):
    #baseDirec="/work/GoryaninU/mitsuki/out/checkm/36m_anode/mycc/out/bins/Cluster.{}".format(clusterNum)
    #baseDirec="/work/GoryaninU/mitsuki/out/checkm/36m_anode/metagen/out/bins/bin{:03d}".format(clusterNum)
    #baseDirec="/work/GoryaninU/mitsuki/out/checkm/36m_anode/refine/out/bins/ref{:03d}".format(clusterNum)
    queryFilepath="/work/GoryaninU/mitsuki/mizuho/genome/faa/ref{:03d}.faa".format(clusterNum)
    outFilepath="/work/GoryaninU/mitsuki/mizuho/genome/m8/transfer/ref{:03d}.m8".format(clusterNum)
    print("{},{},{}".format(dbFilepath, queryFilepath, outFilepath))
