#!/usr/bin/env bash
DATASET_PATH="dataset/creditcard.csv"
DATA_SPLIT_PATH="dataset/xgboost_creditcard/5_exponential/data_site-1.json"
SITE_NUM=5

if [ ! -f "${DATA_SPLIT_PATH}" ]
then
    echo "Please check if you saved CridetCardFraud split json in ${DATA_SPLIT_PATH}"
fi

python3 ../utils/baseline_individual.py --num_parallel_tree 5 --subsample 0.8 --data_path "${DATASET_PATH}" --data_split_path "${DATA_SPLIT_PATH}" --site_num "${SITE_NUM}"
