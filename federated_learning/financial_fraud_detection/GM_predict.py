import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import json
import numpy as np
model_xgb = xgb.Booster()
model_xgb.load_model("./tree-based/workspaces/xgboost_workspace_5_bagging_exponential_split_scaled_lr/simulate_job/app_server/xgboost_model.json")

def _read_Dataset_with_pandas(data_path):
    data = pd.read_csv(data_path, skip_blank_lines=True)
    data_num = data.shape[0]

    # Feature scaling 
    data["normalizedAmount"] = StandardScaler().fit_transform(data["Amount"].values.reshape(-1,1))
    data = data.drop(["Amount"],axis=1)
    data = data.drop(["Time"],axis=1)


    # split to feature and label
    x = data.iloc[:, data.columns != 'Class'].copy()
    y = data.iloc[:, data.columns == 'Class'].copy()
    return x, y, data_num
if __name__ == "__main__":
    data_path = "./dataset/creditcard.csv"

    # training
    X, y, total_train_data_num = _read_Dataset_with_pandas(
        data_path=data_path
    )


    # validation
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, stratify=y)

    inputs = X_val[2:3]
    label = y_val[2:3]

    print("input: ")
    print(inputs)
    print("Ground truth: ")
    print(label)
    pred = xgb.DMatrix(inputs)
    predict_result = model_xgb.predict(pred)
    predict_result = np.round(predict_result)
    print("predict_result: ", int(predict_result[0]))