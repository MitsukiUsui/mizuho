#!/usr/bin/env python3

import pandas as pd

dbDirec="/work/GoryaninU/Askarbek/Pipeline/Tools/kaiju/kaijudb"
dmpFilepath="{}/nodes.dmp".format(dbDirec)

pairFilepath="pair.list"
pair_df=pd.read_csv(pairFilepath)
for _,row in pair_df.iterrows():
    leftFilepath=row["left_filepath"]
    rightFilepath=row["right_filepath"]
   
    #submit with refseq database
    dbFilepath="{}/kaiju_db.fmi".format(dbDirec)
    outFilepath="/work/GoryaninU/mitsuki/out/kaiju/refseq/{}.tsv".format(row["sample_id"])
    print("{},{},{},{},{}".format(dmpFilepath, dbFilepath, leftFilepath, rightFilepath, outFilepath))
    
    #submit with nr
    dbFilepath="{}/kaiju_db_nr_euk.fmi".format(dbDirec)
    outFilepath="/work/GoryaninU/mitsuki/out/kaiju/nr/{}.tsv".format(row["sample_id"])
    print("{},{},{},{},{}".format(dmpFilepath, dbFilepath, leftFilepath, rightFilepath, outFilepath))
