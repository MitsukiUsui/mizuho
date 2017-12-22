#!/usr/bin/env python3

import sys
import pandas as pd
from MapDbController import MapDbController
        
def main(dbFilepath, statFilepath):
    mdc=MapDbController(dbFilepath)
    total=mdc.count_row("read")
    
    dct_lst=[]
    for mapper in ("bowtie",):
        dct={"total": total, "mapper": mapper}
        dct["map_0"]=mdc.calc_mappability(mapper, 1)
        dct["map_3"]=mdc.calc_mappability(mapper, 1000)
        dct["map_4"]=mdc.calc_mappability(mapper, 10000)
        dct["map_5"]=mdc.calc_mappability(mapper, 100000)
        dct["map_6"]=mdc.calc_mappability(mapper, 1000000)
        dct_lst.append(dct)
    stat_df=pd.DataFrame(dct_lst)
    stat_df=stat_df[["total", "mapper", "map_0", "map_3", "map_4", "map_5", "map_6"]]
    stat_df.to_csv(statFilepath, index=False)
    
if __name__=="__main__":
    dbFilepath=sys.argv[1]
    statFilepath=sys.argv[2]
    main(dbFilepath, statFilepath)
