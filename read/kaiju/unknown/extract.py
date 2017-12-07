#!/usr/bin/env python3

import pandas as pd

kaijuFilepath="/work/GoryaninU/mitsuki/out/kaiju/refseq/MFC1_06m_anode_felt_1.tsv"
kaiju_df=pd.read_csv(kaijuFilepath, delimiter="\t", header=None)
for readName in kaiju_df[kaiju_df[0]=="U"][1]:
    print(readName)
