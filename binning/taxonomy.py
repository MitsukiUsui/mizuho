#!/usr/bin/env python3

import pandas as pd
from Bio import SeqIO
import numpy as np

def get_result_df(resultFilepath):
    """
    parse metagen output into DataFrame
    """
    
    dct_lst=[]
    with open(resultFilepath, "r") as f:
        for line in f:
            dct={}
            dct["key"]=(line.strip().split()[0])[2:-1] #">seqId"
            dct["bin_id"]=int((line.strip().split()[1])[1:-1])  #"binId"
            dct_lst.append(dct)
    result_df=pd.DataFrame(dct_lst)
    result_df["bin_id"]=result_df["bin_id"].astype(int)
    return result_df

def main():
    taxonomyFilepath="/work/GoryaninU/mitsuki/out/taxonomy/mmseqs_pool/taxonomy_scaffold.csv"
    tax_df=pd.read_csv(taxonomyFilepath)

    key_lst=[]
    for assemname, scaffname in zip(tax_df["assembly_name"], tax_df["scaffold_name"]):
        key="{}_sc{:05d}".format(assemname, int(scaffname[2:]))
        key_lst.append(key)
    tax_df["key"]=key_lst
    
    df_lst=[]
    for assemname in sorted(set(tax_df["assembly_name"])):
        metagenDirec="/work/GoryaninU/mitsuki/out/binning/metagen/{}".format(assemname)
        resultFilepath="{}/output/segs.txt".format(metagenDirec)
        df_lst.append(get_result_df(resultFilepath))
    result_df=pd.concat(df_lst)

    out_df=pd.merge(tax_df, result_df, on="key", how="left")
    out_df=out_df[["assembly_name","bin_id","scaffold_name", "superkingdom", "phylum", "class", "order", "family", "genus", "species"]]
    
    out_df["bin_id"]=out_df["bin_id"].astype(int)
    out_df=out_df.sort_values(by=["assembly_name", "bin_id", "scaffold_name"], ascending=True)
    outFilepath="taxonomy_bin.csv"
    out_df.to_csv(outFilepath, index=False)


if __name__=="__main__":
    main()

