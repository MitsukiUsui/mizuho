#!/usr/bin/env python3

import os
import pickle
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
        #print("ERROR: unknown taxid = {}".format(taxid))
        return dict()

def get_taxid_lst(accessionVersion_lst):
    from dbcontroller import DbController
    dc = DbController("/work/GoryaninU/mitsuki/blast/accession2taxid/prot.accession2taxid.db")
    
    #  create accession2taxid lookup dictionaly first
    accessionVersion_set=set(accessionVersion_lst)
    accession2taxid=dict()
    print("START: assign taxid to {} unique accession".format(len(accessionVersion_set)), flush=True)
    batch=len(accessionVersion_set)*0.01 #1% of total lines
    border=batch
    for _,accessionVersion in enumerate(accessionVersion_set):
        if _>=border:
            border+=batch
            print(".", end="", flush=True)
        accession2taxid[accessionVersion]=dc.accession2taxid(accessionVersion)
    print()
    
    taxid_lst=[accession2taxid[accessionVersion] for accessionVersion in accessionVersion_lst]
    return taxid_lst
    
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

def main(bestFilepath, geneFilepath):
    best_df=pd.read_csv(bestFilepath, delimiter='\t', header=None)
    
    taxid_lst=get_taxid_lst(list(best_df[1]))
    tax_df=get_tax_df(taxid_lst)
    
    out_df=pd.concat([best_df, tax_df], axis=1)
    assert out_df.shape[0]==best_df.shape[0]
    columns_lst=list(out_df.columns)
    out_df["assembly_name"]=[queryId.split(":")[0] for queryId in best_df[0]]
    out_df["scaffold_name"]=[queryId.split(":")[1] for queryId in best_df[0]]
    out_df=out_df[["assembly_name", "scaffold_name"] + columns_lst]
    
    out_df.to_csv(geneFilepath, index=False)
    print("DONE: output to {}".format(geneFilepath))
    
if __name__=="__main__":
    baseDirec="/work/GoryaninU/mitsuki/out/taxonomy"
    mmseqsDirec="{}/mmseqs_pool".format(baseDirec)
    bestFilepath="{}/result.best".format(mmseqsDirec)
    geneFilepath="{}/taxonomy_gene.csv".format(mmseqsDirec)
    main(bestFilepath, geneFilepath)
