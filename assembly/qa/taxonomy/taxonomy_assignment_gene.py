#!/usr/bin/env python3

import os
import pickle
from ete3 import NCBITaxa
from collections import Counter
import pandas as pd

from dbcontroller import DbController
ncbi = NCBITaxa()

def translator(taxid):
    """
    given taxid, return scientific name
    """
    return ncbi.get_taxid_translator([taxid])[taxid]
    
def get_lineage(taxid, rank_lst = None):
    if rank_lst is None:
        rank_lst=["superkingdom", "phylum", "class", "order", "family", "genus", "species"]
    dct={}
    try:
        for taxidLineage, rank in ncbi.get_rank(ncbi.get_lineage(taxid)).items():
            if rank in rank_lst:
                dct[rank]=taxidLineage
                dct[rank+"_s"]=translator(taxidLineage)
        return dct
    except:
        print("ERROR: unknown taxid = {}".format(taxid))
        return dict()

def read_accession2taxid():
    filepath="/work/GoryaninU/mitsuki/blast/accession2taxid/prot.accession2taxid"
    pickleFilepath="{}.pickle".format(filepath)
    if os.path.exists(pickleFilepath):
        with open(pickleFilepath, 'rb') as handle:
            print("START: read {}".format(pickleFilepath))
            accession2taxid = pickle.load(handle)
            return accession2taxid
    else:
        accession2taxid={}
        print("START: read {}".format(filepath))

        batch=456217760*0.01 #1% of total lines
        border=batch
        with open(filepath, "r") as f:
            f.readline()  #skip header
            for _,line in enumerate(f):
                if _>=border:
                    border+=batch
                    print(".",end="", flush=True)
                accession, _, taxid, _ = line.strip().split()
                accession2taxid[accession]=taxid
        print()
        
        with open(pickleFilepath, 'wb') as handle:
            print("START: write to {}".format(pickleFilepath))
            pickle.dump(accession2taxid, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return accession2taxid

def get_tax_df(taxid_lst):
    rank_lst=["superkingdom", "phylum", "class", "order", "family", "genus", "species"]
    
    #  create taxid2lineage lookup dictionaly first
    taxid_set=set(taxid_lst)
    taxid2lineage=dict()
    print("START: assign lineage to {} unique taxids".format(len(taxid_set)), flush=True)
   
    batch=len(taxid_set)*0.01 #1% of total lines
    border=batch
    for _,taxid in enumerate(taxid_set):
        if _>=border:
            border+=batch
            print(".", end="", flush=True)
        taxid2lineage[taxid]=get_lineage(taxid, rank_lst)
    print()
    
    #  crete tax_df using taxid2lineage
    dct_lst=[]
    for _,taxid in enumerate(taxid_lst):    
        dct={}
        dct["taxid"]=taxid
        dct.update(taxid2lineage[taxid])
        dct_lst.append(dct)
    
    tax_df=pd.DataFrame(dct_lst)
    column_lst=["taxid"]+rank_lst+[rank+"_s" for rank in rank_lst]
    tax_df=tax_df[column_lst]
    tax_df[rank_lst]=tax_df[rank_lst].fillna(0).astype(int)
    
    assert tax_df.shape[0]==len(taxid_lst)
    return tax_df

def main(baseDirec):
    bestFilepath="{}/mmseqs/result.best".format(baseDirec)
    best_df=pd.read_csv(bestFilepath, delimiter='\t', header=None)
    
    dc = DbController("/work/GoryaninU/mitsuki/blast/accession2taxid/prot.accession2taxid.db")
    taxid_lst=dc.accession2taxid(list(best_df[1]))
    tax_df=get_tax_df(taxid_lst)
    
    out_df=pd.concat([best_df, tax_df], axis=1)
    assert out_df.shape[0]==best_df.shape[0]
    out_df["assembly_name"]=[queryId.split(":")[0] for queryId in best_df[0]]
    out_df["scaffold_name"]=[queryId.split(":")[1] for queryId in best_df[0]]
    
    print("START: output")
    for assemname in sorted(set(out_df["assembly_name"])):
        assem_df=out_df[out_df["assembly_name"]==assemname]
        for scaffname in sorted(set(assem_df["scaffold_name"])):
            scaff_df=assem_df[assem_df["scaffold_name"]==scaffname]
            outFilepath="{}/{}/{}/taxonomy.csv".format(baseDirec, assemname, scaffname)
            scaff_df.to_csv(outFilepath, index=False)
            print("\t{}".format(outFilepath))

if __name__=="__main__":
    baseDirec="/work/GoryaninU/mitsuki/out/taxonomy"
    main(baseDirec)
