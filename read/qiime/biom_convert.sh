workDirec=./36m_anode_ref
abundanceTsv=${workDirec}/abundance.tsv
sampleTsv=${workDirec}/sample.tsv
outBiom=${abundanceTsv/.tsv/.biom}
outQza=${abundanceTsv/.tsv/.qza}
outQzv=${abundanceTsv/.tsv/.qzv}
metrixDirec=${workDirec}/core-metrics-results

source activate qiime2-2017.11.2

#--------------------------------------------------------------------------------
# convert to biom format
#--------------------------------------------------------------------------------
#tmpBiom=${outBiom}.tmp
#biom convert --table-type="OTU table" --to-json \
#             -i ${abundanceTsv} -o ${tmpBiom}
#echo "DONE: output ${tmpBiom}"
#biom add-metadata --output-as-json \
#                  -i ${tmpBiom} -o ${outBiom} \
#                  --sample-metadata-fp ${sampleTsv}
##                  --observation-metadata-fp ${taxonomyTsv}
#rm ${tmpBiom}
#echo "DONE: output ${outBiom}"
#
#
##--------------------------------------------------------------------------------
## convert to qiime format
##--------------------------------------------------------------------------------
#qiime tools import \
#  --input-path ${outBiom} \
#  --type 'FeatureTable[Frequency]' \
#  --source-format BIOMV100Format \
#  --output-path ${outQza}
#echo "DONE: output ${outQza}"
#
#qiime feature-table summarize \
#    --i-table ${outQza} \
#    --o-visualization ${outQzv}
#echo "DONE: output ${outQzv}"


#--------------------------------------------------------------------------------
# output metrix
#--------------------------------------------------------------------------------
qiime diversity core-metrics \
    --i-table ${outQza} \
    --p-sampling-depth 600000 \
    --m-metadata-file ${sampleTsv} \
    --output-dir ${metrixDirec}
#echo "DONE: output core metrix to ${metrixDirec}"

source deactivate
