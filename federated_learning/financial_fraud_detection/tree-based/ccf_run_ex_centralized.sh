#!/usr/bin/env bash
DATASET_PATH="/Users/cheng/LAB/TTC/NVFlare/examples/advanced/xgboost/dataset/creditcard.csv"
SITE_NUM=5

if [ ! -f "${DATASET_PATH}" ]
then
    echo "Please check if you saved HIGGS dataset in ${DATASET_PATH}"
fi

#python3 ../utils/baseline_centralized.py --num_parallel_tree 1 --data_path "${DATASET_PATH}"

python3 ../utils/baseline_centralized.py --num_parallel_tree 5 --subsample 0.8 --data_path "${DATASET_PATH}" --site_num "${SITE_NUM}"

#python3 ../utils/baseline_centralized.py --num_parallel_tree 5 --subsample 0.2 --data_path "${DATASET_PATH}"
#python3 ../utils/baseline_centralized.py --num_parallel_tree 20 --subsample 0.05 --data_path "${DATASET_PATH}"
#python3 ../utils/baseline_centralized.py --num_parallel_tree 20 --subsample 0.8 --data_path "${DATASET_PATH}"
