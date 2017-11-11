#!/usr/bin/env python3

from ete3 import NCBITaxa
from collections import Counter
import pandas as pd
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
    filepath="/work/GoryaninU/mitsuki/blast/accession2taxid/prot.accession2taxid.head"
    accession2taxid={}
    print("START: read {}".format(filepath))
    
    batch=456217760*0.1 #10% of total lines
    border=batch
    with open(filepath, "r") as f:
        f.readline()  #skip header
        for _,line in enumerate(f):
            if _>=border:
                border+=batch
                print(".",end="")
            accession, _, taxid, _ = line.strip().split()
            accession2taxid[accession]=taxid
    print()
    return accession2taxid
    
def main(filepath):
    accession2taxid=read_accession2taxid()
    
    rank_lst=["superkingdom", "phylum", "class", "order", "family", "genus", "species"]
    df=pd.read_csv(filepath, delimiter='\t', header=None)
    dct_lst=[]
    
    print("START: process {}".format(filepath))
    batch=df.shape[0]*0.1 #10% of total lines
    border=batch
    for _,accession in enumerate(df[1]):
        if _>=border:
            border+=batch
            print(".", end="")
        
        accession=accession.split(".")[0]
        dct={}
        if accession in accession2taxid:
            taxid=accession2taxid[accession]
            dct["taxid"]=taxid
            dct.update(get_lineage(taxid, rank_lst))
        else:
            dct["taxid"]=0
        dct_lst.append(dct)
    print()
    
    tax_df=pd.DataFrame(dct_lst)
    column_lst=["taxid"]+rank_lst+[rank+"_s" for rank in rank_lst]
    tax_df=tax_df[column_lst]
    tax_df[rank_lst]=tax_df[rank_lst].fillna(0).astype(int)
    
    assert tax_df.shape[0]==df.shape[0]
    out_df=pd.concat([df, tax_df], axis=1)
    assert out_df.shape[0]==df.shape[0]
    out_df["assembly_name"]=[queryId.split(":")[0] for queryId in df[0]]
    out_df["scaffold_name"]=[queryId.split(":")[1] for queryId in df[0]]
    
    print("START: output")
    for assemname in sorted(set(out_df["assembly_name"])):
        assem_df=out_df[out_df["assembly_name"]==assemname]
        for scafname in sorted(set(assem_df["scaffold_name"])):
            scaf_df=assem_df[assem_df["scaffold_name"]==scafname]
            outFilepath="./tmp/{}/{}/taxonomy.csv".format(assemname, scafname)
            scaf_df.to_csv(outFilepath, index=False)
            print("\t{}".format(outFilepath))

if __name__=="__main__":
    filepath="./tmp/mmseqs/result.best.head"
    main(filepath)
