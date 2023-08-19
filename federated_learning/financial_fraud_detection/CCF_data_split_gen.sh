#!/usr/bin/env bash
DATASET_PATH="/Users/cheng/LAB/TTC/NVFlare/examples/advanced/xgboost/dataset/creditcard.csv"
OUTPUT_PATH="/Users/cheng/LAB/TTC/NVFlare/examples/advanced/xgboost/dataset/xgboost_creditcard"

if [ ! -f "${DATASET_PATH}" ]
then
    echo "Please check if you saved creditcard dataset in ${DATASET_PATH}"
fi

echo "Generated creditcard data splits, reading from ${DATASET_PATH}"
for site_num in 2 5 20;
do
    for split_mode in uniform exponential square linear IID;
    do
        python3 utils/prepare_data_split.py \
        --data_path "${DATASET_PATH}" \
        --site_num ${site_num} \
        --size_total 284807 \
        --size_valid 49841 \
        --split_method ${split_mode} \
        --out_path "${OUTPUT_PATH}/${site_num}_${split_mode}"
    done
done
echo "Data splits are generated in ${OUTPUT_PATH}"

#total dataset 284807
