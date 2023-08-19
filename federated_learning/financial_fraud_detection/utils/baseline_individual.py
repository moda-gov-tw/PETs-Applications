# Author HC_SU
# Project TTC PPFL
# Model XGB
# Dataset CreditCardFraud@Kaggle.com
# Discribe: everyone gets the same distribution dataset as well as the label ratio
import json

import argparse
import os
import tempfile
import time

import pandas as pd
import xgboost as xgb
from sklearn.metrics import roc_auc_score
from torch.utils.tensorboard import SummaryWriter

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def xgboost_args_parser():
    parser = argparse.ArgumentParser(description="Individual XGBoost training with random forest options")
    parser.add_argument("--data_path", type=str, default="./dataset/creditcard.csv", help="path to dataset file")
    parser.add_argument("--data_split_path", type=str, default="./dataset/xgboost_creditcard/5_exponential/data_site-1.json", help="path to dataset file")
    parser.add_argument("--num_parallel_tree", type=int, default=1, help="num_parallel_tree for random forest setting")
    parser.add_argument("--subsample", type=float, default=1, help="subsample for random forest setting")
    parser.add_argument("--num_rounds", type=int, default=100, help="number of boosting rounds")
    parser.add_argument("--workspace_root", type=str, default="workspaces", help="workspaces root")
    parser.add_argument("--tree_method", type=str, default="hist", help="tree_method")
    parser.add_argument("--train_in_one_session", action="store_true", help="whether to train in one session")
    parser.add_argument("--site_num", type=int, help="Total number of sites")

    return parser


def prepare_creditcard(data_path):
    creditcard = pd.read_csv(data_path, skip_blank_lines=True)
    # print(creditcard.info())
    # print(creditcard.head())
    total_data_num = creditcard.shape[0]

    print(f"Total data count: {total_data_num}")
    
    # Feature scaling 
    creditcard['normalizedAmount'] = StandardScaler().fit_transform(creditcard['Amount'].values.reshape(-1,1))
    creditcard = creditcard.drop(['Amount'], axis=1)
    creditcard = creditcard.drop(['Time'], axis=1)

    # split to feature and label
    X = creditcard.iloc[:, creditcard.columns != 'Class']
    y = creditcard.iloc[:, creditcard.columns == 'Class']
    print("Label counts: ")
    print(y.value_counts())
    return X, y, total_data_num


def train_one_by_one(train_data, val_data, xgb_params, num_rounds, val_label, writer: SummaryWriter):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_model_path = os.path.join(tmp_dir, "model.json")
        # Round 0
        print("Round: 0 Base ", end="")
        bst = xgb.train(
            xgb_params, train_data, num_boost_round=1, evals=[(val_data, "validate"), (train_data, "train")]
        )
        bst.save_model(tmp_model_path)
        for r in range(1, num_rounds):
            # Validate the last round's model
            bst_last = xgb.Booster(xgb_params, model_file=tmp_model_path)
            y_pred = bst_last.predict(val_data)
            roc = roc_auc_score(val_label, y_pred)
            print(f"Round: {bst_last.num_boosted_rounds()} model testing AUC {roc}")
            writer.add_scalar("AUC", roc, r - 1)
            # Train new model
            print(f"Round: {r} Base ", end="")
            bst = xgb.train(
                xgb_params,
                train_data,
                num_boost_round=1,
                xgb_model=tmp_model_path,
                evals=[(val_data, "validate"), (train_data, "train")],
            )
            bst.save_model(tmp_model_path)
        return bst


def get_training_parameters(args):
    # use logistic regression loss for binary classification
    # use auc as metric
    param = {
        "objective": "binary:logistic",
        "eta": 0.1,
        "max_depth": 8,
        "eval_metric": "auc",
        "nthread": 16,
        "num_parallel_tree": args.num_parallel_tree,
        "subsample": args.subsample,
        "tree_method": args.tree_method,
    }
    return param

def gen_site_list(site_num):
    site_list = [""]*site_num
    for i in range(site_num):
        site_list[i] = "site-" + str(i+1)
    return site_list

import numpy as np
def train_split(train_data_split_dict, val_data_split_dict, site_num, X, y):
    # Calculate the number of samples per fold
    samples_per_fold = len(X) // site_num

    # # Shuffle the data and labels 打亂
    # indices = np.arange(len(X))
    # np.random.shuffle(indices)
    # X_shuffled = X.iloc[indices]
    # y_shuffled = y.iloc[indices]

    for fold in range(site_num):
        # Get the start and end indices for the current fold
        start_idx = fold * samples_per_fold
        end_idx = start_idx + samples_per_fold

        # Split the data and labels for the current fold
        # X_fold = X_shuffled[start_idx:end_idx]    #有經過打亂
        # y_fold = y_shuffled[start_idx:end_idx]    #有經過打亂
        X_fold = X[start_idx:end_idx]
        y_fold = y[start_idx:end_idx]

        # Split the current fold into training and validation sets
        X_train, X_val, y_train, y_val = train_test_split(X_fold, y_fold, test_size=0.1, stratify=y_fold)

        # Store the data and labels in the dictionaries with appropriate keys
        site_name = f"site-{fold+1}"
        train_data_split_dict[site_name] = (X_train, y_train)
        val_data_split_dict[site_name] = (X_val, y_val)

        # Print the size and class proportions for the current fold
        print(f"{site_name} Data Split - X_train: {len(X_train)}, X_val: {len(X_val)}")
        print("Class Proportions:")
        print(y_train.value_counts(normalize=True))
        print(y_val.value_counts(normalize=True))

def main():
    parser = xgboost_args_parser()
    args = parser.parse_args()
    data_path = args.data_path
    site_num = args.site_num
    site_list = gen_site_list(site_num)

    # 建立字典來存放分割後的資料集
    train_data_split_dict = {}
    val_data_split_dict = {}
    # Load data
    start = time.time()
    print(" Data spliting Start")
    X, y, total_train_data_num = prepare_creditcard(data_path)
    # data_per_fold = total_train_data_num/site_num
    # 分割各個site的資料
    train_split(train_data_split_dict, val_data_split_dict, site_num, X, y)

    end = time.time()
    lapse_time = end - start
    print(" Data spliting Done")
    print(f"Data spliting time: {lapse_time}")

    for site in site_list:
        # Specify training params
        if args.train_in_one_session:
            model_name = site + "_simple_" + str(args.num_parallel_tree) + "_" + str(args.subsample)
        else:
            model_name = site + "_" + str(args.num_parallel_tree) + "_" + str(args.subsample)

        
        num_rounds = args.num_rounds
        # valid_num = 49841
        exp_root = os.path.join(args.workspace_root, model_name)
        # Set mode file paths
        model_path = os.path.join(exp_root, "model.json")
        # Set tensorboard output
        writer = SummaryWriter(exp_root)

        # Load data
        start = time.time()
        print(site + " Data Loading...")
        X_train, y_train = train_data_split_dict[site]
        X_valid, y_valid = val_data_split_dict[site]
        # construct training and validation xgboost DMatrix
        dmat_train = xgb.DMatrix(X_train, label=y_train)     
        dmat_valid = xgb.DMatrix(X_valid, label=y_valid)  
        end = time.time()         
        lapse_time = end - start
        print(site + " Data Loading Done")
        print(f"Data loading time: {lapse_time}")


        # setup parameters for xgboost
        xgb_params = get_training_parameters(args)

        # xgboost training
        print(site + " Start Training")
        start = time.time()
        if args.train_in_one_session:
            bst = xgb.train(
                xgb_params, dmat_train, num_boost_round=num_rounds, evals=[(dmat_valid, "validate"), (dmat_train, "train")]
            )
        else:
            bst = train_one_by_one(
                train_data=dmat_train,
                val_data=dmat_valid,
                xgb_params=xgb_params,
                num_rounds=num_rounds,
                val_label=y_valid,
                writer=writer,
            )

        bst.save_model(model_path)
        end = time.time()
        lapse_time = end - start
        print(site + " Training Done")
        print(f"Training time: {lapse_time}")

        # test model
        bst = xgb.Booster(xgb_params, model_file=model_path)
        y_pred = bst.predict(dmat_valid)
        roc = roc_auc_score(y_valid, y_pred)
        print(f"Base model: {roc}")
        writer.add_scalar("AUC", roc, num_rounds - 1)
        writer.close()

       


if __name__ == "__main__":
    main()
