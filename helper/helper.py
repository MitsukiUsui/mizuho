import yaml

def get_sampleId_lst(yamlFilepath):
    with open(yamlFilepath, 'r') as f:
        yml=yaml.load(f)
    filepath_lst=yml[0]["left reads"] # assume all the same with yml[0]["right reads"]
    sampleId_lst=[filepath.split('/')[-1].replace(".fastq", "")[:-3]  for filepath in filepath_lst] #-3 to remove direction
    return sampleId_lst
