# Author HC_SU
# Project TTC PPFL
# Model XGB
# Dataset CreditCardFraud@Kaggle.com
import json

import pandas as pd
import xgboost as xgb

from sklearn.preprocessing import StandardScaler
from nvflare.app_common.app_constant import AppConstants
from nvflare.app_opt.xgboost.tree_based.executor import FedXGBTreeExecutor


def _read_Dataset_with_pandas(data_path, start: int, end: int):
    data_size = end - start
    data = pd.read_csv(data_path, header=None, skiprows=start, nrows=data_size, skip_blank_lines=True)
    data_num = data.shape[0]

    # Feature scaling 
    data['normalizedAmount'] = StandardScaler().fit_transform(data['Amount'].values.reshape(-1,1))
    data = data.drop(['Amount'],axis=1)
    data = data.drop(['Time'],axis=1)

    # split to feature and label
    x = data.iloc[:, df.columns != 'Class'].copy()
    y = data.iloc[:, df.columns == 'Class'].copy()

    return x, y, data_num


class FedXGBTreeCreditCardExecutor(FedXGBTreeExecutor):
    def __init__(
        self,
        data_split_filename,
        training_mode,
        lr_scale,
        num_client_bagging: int = 1,
        lr_mode: str = "uniform",
        local_model_path: str = "model.json",
        global_model_path: str = "model_global.json",
        learning_rate: float = 0.1,
        objective: str = "binary:logistic",
        num_local_parallel_tree: int = 1,
        local_subsample: float = 1,
        max_depth: int = 8,
        eval_metric: str = "auc",
        nthread: int = 16,
        tree_method: str = "hist",
        train_task_name: str = AppConstants.TASK_TRAIN,
    ):
        super().__init__(
            training_mode=training_mode,
            num_client_bagging=num_client_bagging,
            lr_scale=lr_scale,
            lr_mode=lr_mode,
            local_model_path=local_model_path,
            global_model_path=global_model_path,
            learning_rate=learning_rate,
            objective=objective,
            num_local_parallel_tree=num_local_parallel_tree,
            local_subsample=local_subsample,
            max_depth=max_depth,
            eval_metric=eval_metric,
            nthread=nthread,
            tree_method=tree_method,
            train_task_name=train_task_name,
        )
        self.data_split_filename = data_split_filename

    def load_data(self):
        with open(self.data_split_filename) as file:
            data_split = json.load(file)

        data_path = data_split["data_path"]
        data_index = data_split["data_index"]

        # check if site_id and "valid" in the mapping dict
        if self.client_id not in data_index.keys():
            raise ValueError(
                f"Dict of data_index does not contain Client {self.client_id} split",
            )

        if "valid" not in data_index.keys():
            raise ValueError(
                "Dict of data_index does not contain Validation split",
            )

        site_index = data_index[self.client_id]
        valid_index = data_index["valid"]

        # training
        X_train, y_train, total_train_data_num = _read_Dataset_with_pandas(
            data_path=data_path, start=site_index["start"], end=site_index["end"]
        )
        xgbc = xgb.XGBClassifier()
        dmat_train = xgbc.fit(X = X_train, y = y_train)

        # validation
        X_valid, y_valid, total_valid_data_num = _read_Dataset_with_pandas(
            data_path=data_path, start=valid_index["start"], end=valid_index["end"]
        )
        dmat_valid = xgbc.fit(X = X_valid, y = y_valid)

        return dmat_train, dmat_valid
