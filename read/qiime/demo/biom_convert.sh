abundanceTsv=abundance.tsv
sampleTsv=sample.tsv
outBiom=abundance.biom
outQza=abundance.qza
outQzv=abundance.qzv

tmpBiom=${outBiom}.tmp
biom convert --table-type="OTU table" --to-json \
             -i ${abundanceTsv} -o ${tmpBiom}
echo "DONE: output ${tmpBiom}"
biom add-metadata --output-as-json \
                  -i ${tmpBiom} -o ${outBiom} \
                  --sample-metadata-fp ${sampleTsv}
#                  --observation-metadata-fp ${taxonomyTsv}
#rm ${tmpBiom}
echo "DONE: output ${outBiom}"

qiime tools import \
  --input-path ${outBiom} \
  --type 'FeatureTable[Frequency]' \
  --source-format BIOMV100Format \
  --output-path ${outQza}
echo "DONE: output ${outQza}"

qiime feature-table summarize \
    --i-table ${outQza} \
    --o-visualization ${outQzv}
echo "DONE: output ${outQzv}"
