import pandas as pd

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
