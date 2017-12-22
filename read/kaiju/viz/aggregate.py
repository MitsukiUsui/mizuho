#! /usr/bin/env python3

from ete3 import NCBITaxa
from collections import Counter
import pandas as pd
ncbi = NCBITaxa()

def output_abundance(abundanceFilepath, dct_lst):
    """
    one column per one sample, one row per one taxid
    """
    
    out_df = pd.DataFrame(dct_lst)
    out_df=out_df.set_index("sample_id")
    out_df=out_df.fillna(0)
    out_df=out_df[out_df.columns].astype(int)
    out_df=out_df.transpose()
    out_df.index.name="taxid"
    out_df.to_csv(abundanceFilepath, sep="\t")

def output_taxonomy(taxFilepath, taxid_set):
    """
    output taxid with taxstr
    """
    
    def translator(taxid):
        return ncbi.get_taxid_translator([taxid])[taxid]
    
    def get_taxstr(taxid):
        if taxid==0:
            return "Root;k__unclassified"
        
        rank_lst=["superkingdom", "phylum", "class", "order", "family", "genus", "species"]
        prefix_lst=["k__","p__","c__","o__","f__","g__","s__"]
        assert len(rank_lst)==len(prefix_lst)
        name_lst=["" for _ in range(len(rank_lst))] #posess each name for each rank

        for _taxid, rank in ncbi.get_rank(ncbi.get_lineage(taxid)).items():
            if rank in rank_lst:
                name_lst[rank_lst.index(rank)]=translator(_taxid)
        
        taxstr = "Root"
        for prefix, name in zip(prefix_lst, name_lst):
            if name == "":
                if taxstr == "Root":
                    taxstr = "Root;k__unclassified"
                break
            taxstr += ";" + prefix + name
        return taxstr
    
    with open(taxFilepath, 'w') as f:
        header="#{}\t{}\n".format("TAXID", "taxonomy")
        f.write(header)

        for _, taxid in enumerate(taxid_set):
            line = "{}\t{}\n".format(taxid, get_taxstr(taxid))
            f.write(line)
    

def main(sampleFilepath, abundanceFilepath, taxFilepath):
    sample_df=pd.read_csv(sampleFilepath, delimiter="\t")

    dct_lst=[] #for abundace
    taxid_set = set() # for taxonomy
    
    print("START: parse {} kaiju outputs".format(sample_df.shape[0]))
    for _, row in sample_df.iterrows():
        print("\t{}".format(row["filepath"]))
        
        kaiju_df=pd.read_csv(row["filepath"], delimiter="\t", header=None)
        taxid_lst=list(kaiju_df[2])

        #update dct_lst
        dct={}
        dct["sample_id"]=row["sampleID"]
        for taxid, abundance in Counter(taxid_lst).items():
            dct[taxid]=abundance
        dct_lst.append(dct)

        # update taxid_set
        taxid_set.update(taxid_lst)
        
    print("START: output abundance to {}".format(abundanceFilepath), flush=True)
    output_abundance(abundanceFilepath, dct_lst)
    print("START: output taxonomy to {}".format(taxFilepath), flush=True)
    output_taxonomy(taxFilepath, taxid_set)

if __name__=="__main__":
    sampleFilepath="./out/sample.tsv"
    abundanceFilepath = "./out/abundance.tsv"
    taxFilepath = "./out/taxonomy.tsv"
    main(sampleFilepath, abundanceFilepath, taxFilepath)
