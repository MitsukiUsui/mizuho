#!/usr/bin/env python3

import pandas as pd

mapper="bowtie"
assemblyFilepath="assembly.list"
assem_df=pd.read_csv(assemblyFilepath)
for _, row in assem_df.iterrows():
    dbFilepath="/work/GoryaninU/mitsuki/out/map/{}/index/{}".format(mapper, row["assembly_name"])
    print("{},{},{}".format(mapper, row["scaffold_filepath"], dbFilepath))
