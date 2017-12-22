baseDirec=./ref
abundanceTsv=${baseDirec}/abundance.tsv
taxonomyTsv=${baseDirec}/taxonomy.tsv
sampleTsv=${baseDirec}/sample.tsv
outBiom=${baseDirec}/abundance.biom

tmpBiom=${outBiom/.biom/.tmp.biom}
outFold=${outBiom}.fold

biom convert --table-type="OTU table" --to-json \
             -i ${abundanceTsv} -o ${tmpBiom}
biom add-metadata --output-as-json \
                  -i ${tmpBiom} -o ${outBiom} \
                  --sample-metadata-fp ${sampleTsv} \
                  --observation-metadata-fp ${taxonomyTsv}
fold ${outBiom} > ${outFold}

