#!/usr/bin/env python3

import pandas as pd
import sys

sys.path.append("/home/m/mitsuki-usui/mizuho/assembly/qa/map")
from MapDbController import MapDbController

def get_name2id_scaffold(mdc):
    query="SELECT id,name FROM scaffold;"
    success=mdc.execute(query)
    if success:
        results=mdc.cur.fetchall()
        name2id={}
        for result in results:
            name2id[result["name"]]=result["id"]
        return name2id
    else:
        return None

def main(dbFilepath):
    mdc=MapDbController(dbFilepath)
    name2id=get_name2id_scaffold(mdc)
    print("DONE: found {} scaffolds".format(len(name2id)))
    
    name2ref={}
    for refId in range(1, 67 + 1):
        nameFilepath="/work/GoryaninU/mitsuki/mizuho/genome/fna/ref{:03d}.name".format(refId)
        with open(nameFilepath, "r") as f:
            for line in f:
                name=line.strip()
                if name in name2ref.keys():
                    print("WARN: duplicated reference assignment for {} exists".format(name))
                name2ref[line.strip()]=refId
    print("DONE: found {} reference information".format(len(name2ref)))
    assert len(name2id)==len(name2ref)
    
    dct_lst=[]
    for name in name2id.keys():
        dct={}
        dct["scaff_id"]=name2id[name]
        dct["bin_id"]=name2ref[name]
        dct_lst.append(dct)
    ref_df=pd.DataFrame(dct_lst)
    
    query = "CREATE TABLE ref (scaff_id INTEGER PRIMARY KEY, bin_id INTEGER);"
    mdc.execute(query)
    ref_df.to_sql("ref", mdc.con, if_exists="append", index=False)
    print("DONE: create ref table")

if __name__=="__main__":
    sampleId=sys.argv[1]
    dbFilepath="/work/GoryaninU/mitsuki/out/map/db/ref/{}.sq3".format(sampleId)
    main(dbFilepath)
