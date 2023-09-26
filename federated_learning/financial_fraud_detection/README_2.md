
# Privacy-Preserving Research Data Sharing

Credit card fraud is a growing concern worldwide, causing huge financial losses to businesses, banks and individuals. To effectively deal with this problem, Fraud Detection System (FDS) plays an important role. Traditional centralized methods have privacy and security risks, so the joint machine learning training method can achieve collaboration while protecting privacy. Through federated learning, multiple financial institutions cooperate on the basis of a shared model, reducing the risk of sensitive data exposure while obtaining superior model performance.

## Dataset


* Credit Card Fraud Detection data source
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
* Data set introduction:
This dataset contains credit card transactions by European cardholders in September 2013.
Due to confidentiality issues, the public data set cannot provide the original characteristics of the data and more background information. Some field data are converted numerical variables of Principal Components Analysis (PCA), that is, fields V1, V2 to V28 are PCA Transformation results to protect customer information.
PCA is essentially a dimensionality reduction technique that preserves the most important features while reducing the number of dimensions. Therefore, these 28 V variables can be considered as representations of more different variables such as customer details, transaction amount, transaction location, etc.
* Dataset size:
150.83MB
* Dataset field:
Time: The number of seconds elapsed between each transaction and the first transaction in the dataset
V1, V2, …, V28: results transformed by PCA (may contain private data)
Amount: transaction amount
class: 1 in case of fraud, 0 otherwise (target variable for prediction)

![](https://hackmd.io/_uploads/rkfjVI0a2.jpg)


## Used PETs

There are several privacy protection technologies in the current joint learning, which can be adjusted according to the needs of users to meet the security requirements in different environments. Here, the joint learning of the fraud detection system is used as an example for illustration.

* Federated Learning
Through joint learning, customer credit card transaction data scattered in different financial institutions can be trained for a common fraud detection model. Each financial institution uses its own data to train a local model locally, and then uploads the local model to the server for global model aggregation and integration. Update, since the data does not need to be transmitted to the server or third-party centralized, it can protect the privacy of transaction data to different financial institutions.
However, in this case, the server can directly obtain the model parameter update of each financial institution, and external attackers may eavesdrop on the transmission channel to obtain relevant information and conduct inference attacks, which may pose a threat to data privacy. Therefore, when implementing federated learning, it is necessary to consider strengthening data privacy protection measures.

* Differential Privacy (Federal Learning for Privacy Enhanced Protection)
Differential privacy is used to defend against collusion attacks when using secure multi-party operations. Taking 5 financial institutions participating in the training as an example, the collusion attack that may occur is that the server colludes with 4 financial institutions. When this happens, the co-conspirator can recover the actual local model parameters of the uncolluded institutions, so add the difference Privacy enables each local to independently generate random noise and add it to its local model parameters. After adding this random noise to the local model weights, even in the case of 4 financial institutions and the server cooperating, they can only recover the noised local model parameters of the non-colluding institutions, not the actual local model parameters.
However, adding noise can improve the degree of privacy protection, but at the same time, it will affect the accuracy of the model. Therefore, it is necessary to find a balance within a reasonable range of noise to ensure that privacy is properly protected while maintaining reasonable performance of the model, in this way to defend against collusion attacks that may suffer from federated learning that only uses secure multi-party operations.

## Goals of Using PETs

Using **federated learning** to save data in their own local systems reduces the risk of exposing sensitive data, and each local side can benefit from the shared model, which can achieve better model performance than individual training. 

Using **differential privacy** prevents servers from cooperating with data providers to infer private data from information they have about each other, and prevents attackers from eavesdropping on the transmission channel to obtain information for reasoning.

## Data Processing

In the privacy-enhanced joint machine learning architecture, each financial institution participating in the training is regarded as an independent local end. We can use servers on public cloud service platforms (such as AWS, Azure or Google Cloud) as aggregation servers. In order to enhance privacy protection, differential privacy technology is also used, so the training process is as follows:
1.	The local end uses local data to train the model, and adds the obtained local model parameters to the random noise of differential privacy to protect the local model parameters from direct prying by the server.
2.	Upload the protected parametric local model to the aggregation server.
3.	When the server receives the data uploaded by the local end, it aggregates the data and updates the global model after completion. The updated global model will be sent back to all local ends for a new round of training.

![](https://hackmd.io/_uploads/HyTeH80T3.jpg)

## Quick Start

Install NVFLARE:
```
$ python3 -m pip install nvflare
```
Install [Dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/) to ./dataset

Clone repo to get examples(連結待補上):
```
$ git clone https://github.com/
$ cd tree-based
```
Quick Start with Simulator:
Making sure the NVFLARE environment is set up correctly following Installation, you can run an example application with The FL Simulator using the following script
```
$ nvflare simulator jobs/creditcard_5_bagging_HE_exponential_split_scaled_lr -w ${PWD}/workspaces/creditcard_5_bagging_HE_exponential_split_scaled_lr -n 5 -t 5
```

Command Usage:
```
usage: nvflare simulator [-h] -w WORKSPACE [-n N_CLIENTS] [-c CLIENTS] [-t THREADS] [-gpu GPU] job_folder

positional arguments:
job_folder

optional arguments:
-h, --help             show this help message and exit
-w WORKSPACE, --workspace WORKSPACE
WORKSPACE folder
-n N_CLIENTS, --n_clients N_CLIENTS
number of clients
-c CLIENTS, --clients CLIENTS
client names list
-t THREADS, --threads THREADS
number of parallel running clients
-gpu GPU, --gpu GPU
list of GPU Device Ids, comma separated
-m MAX_CLIENTS, --max_clients MAX_CLIENTS
maximum number of clients
```




## Reference
Please refer to [here](https://hackmd.io/@petworks/ByAmydrP3) for the Chinese version of this documentation. 

## Disclaimer
The application listed here only serves as the minimum demonstrations of using PETs. The source code should not be directly deployed for production use.

## Reference


Please refer to [here](https://hackmd.io/@petworks/ByAmydrP3) for the Chinese version of this documentation. 

## Disclaimer

The application listed here only serves as the minimum demonstrations of using PETs. The source code should not be directly deployed for real-world use.
