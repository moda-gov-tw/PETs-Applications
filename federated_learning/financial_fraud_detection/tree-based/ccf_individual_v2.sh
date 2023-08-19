#!/usr/bin/env bash
DATASET_PATH="/Users/cheng/LAB/TTC/NVFlare/examples/advanced/xgboost/dataset/creditcard.csv"
DATA_SPLIT_PATH="/Users/cheng/LAB/TTC/NVFlare/examples/advanced/xgboost/dataset/xgboost_creditcard/5_uniform/data_site-1.json"
SITE_NUM=5

if [ ! -f "${DATA_SPLIT_PATH}" ]
then
    echo "Please check if you saved CridetCardFraud split json in ${DATA_SPLIT_PATH}"
fi

for i in $(seq 1 ${SITE_NUM});
do
   SITE_ID="site-$i"
   echo "This is ${SITE_ID}..."
   python3 ../utils/individual_v2.py --num_parallel_tree 5 --subsample 0.8 --data_path "${DATASET_PATH}" --data_split_path "${DATA_SPLIT_PATH}" --site_id "${SITE_ID}" --site_num "${SITE_NUM}"
done

