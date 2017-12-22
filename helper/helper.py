import yaml
import os
import pandas as pd

def get_sampleId_lst(yamlFilepath):
    with open(yamlFilepath, 'r') as f:
        yml=yaml.load(f)
    filepath_lst=yml[0]["left reads"] # assume all the same with yml[0]["right reads"]
    sampleId_lst=[filepath.split('/')[-1].replace(".fastq", "")[:-3]  for filepath in filepath_lst] #-3 to remove direction
    return sampleId_lst

def get_stat(seqFilepath, key):
    """
    given fastqFilepath, search stat file and return value correspond to key
    """
    
    statFilepath=seqFilepath.split('.fastq')[0] + ".stat"
    if not(os.path.isfile(statFilepath)):
        print("ERROR: stat file not exists, {}".format(statFilepath))
        return None
    stat_df=pd.read_csv(statFilepath, delimiter='\t')
    if not(key in stat_df.columns):
        print("ERROR: key not exists, {}".format(key))
        return None
    return stat_df.loc[0, key]
