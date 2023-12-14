# Criminal Data Cloud Computing

> :exclamation: Please refer [here](https://hackmd.io/@petworks/SJ3i2nq0n) for the Chinese version of the scenario description.

In recent years, the Executive Yuan has organized units across Taiwan to promote the “centralization of information resources,” which means that many units’ servers and other ICT equipment are not managed by themselves but by higher-level units or information management units. Although the centralization method can make the ICT system easier to manage, it also means that the information management unit can easily access the data of the managed servers, creating the possibility of privacy leakage.

As mentioned above, if the various ministries and agencies of the Executive Yuan also want to promote the centralization plan, they will face the same problem. Therefore, we hope to simulate the centralization plan implemented by the crime investigation authority, which will centralize the criminal data to another institution, such as a co-constructed computer room, for management and apply fully homomorphic encryption technology to privacy protection in this simulation scenario. The data to be centralized is encrypted so that the centralizing party cannot obtain the plaintext content of the data and uses the characteristics of fully homomorphic encryption to allow the centralizing party to perform various operations without knowing the plaintext content. In this way, we can solve the above problem and make the centralization plan and privacy protection go hand in hand. In our simulation scenario, we will use the mechanism of fully homomorphic encryption to encrypt all the plaintext crime data of the crime investigation agency (starting now referred to as the client side) and then send it to the co-constructed computer room (starting now referred to as the server side) for storage and computation by the operation agency.
## Dataset

We used the government’s open data platform, which contains crime data, to generate our simulated crime data set for crime investigation agencies. The generated data set has the following fields, as shown in the figure:

1. Name: The actual name of the offender, indicated by * here.
2. Case type: The type of case for each crime.
3. Date: The date of each crime.
4. Location: The location of each crime.
## Used PETs


Fully homomorphic encryption

## Goals of Using PETs


The data centralizer can still perform various calculation operations through fully homomorphic encryption technology because the plaintext data cannot be obtained.

## Data Processing

It is difficult to compute the encrypted data in the most cryptosystem without decrypting it. However, decrypting data is often accompanied by a higher risk of privacy leakage. The fully homomorphic encryption technology is one of the best ways to solve this problem.
The operation of fully homomorphic encryption is shown in the figure below. Let's assume that the owner of the data needs to send the data to another party for computation, then the operation mechanism is as follows:

1. The data owner first encrypts the data to be transmitted with the fully homomorphic encryption technology key and then transmits the ciphertext data to the data operator.
2. After receiving the ciphertext, the data operator can perform corresponding operations on the data under the ciphertext according to the needs of the data owner.
3. After the data operator completes the computation, it sends the ciphertext data back to the data owner after the computation.
4. The data owner can use the decryption key to decrypt the ciphertext after computation to get the required computation result.

The application listed here only serves as the minimum demonstration of using PETs. The source code should not be directly deployed for production use.


## Quick Start

The application has been tested using OpenFHE v1.1.1 and nodejs 20.10.0 on Ubuntu 22.04.3 with Intel(R) Core(TM) i7-10700KF and 32 GB memory.

### Build The Server And Client

#### Step 1. Build and install OpenFHE
If you don't know how to do it, please check
[the OpenFHE documentation](https://openfhe-development.readthedocs.io/en/latest/sphinx_rsts/intro/installation/linux.html).

#### Step 2. Build the source code

Clone the repo and go to the application directory.
```
git clone https://github.com/moda-gov-tw/PETs-Applications
cd PETs-Applications/homomorphic_encryption/criminal_data_cloud_computing/tfhe-police/
```

Create a directory where the executables will be placed and build the application.
```
mkdir build
cd build
cmake ..
make
```

Copy the dataset to the current directory.
```
cp ../testing/data.csv .
```

### Build The Network Service

#### Step 1. Prepare the server executable

Please follow the above instructions to build the server. 

Then, create a directory named `uploads` in the `node.js` directory and copy the server into it.
```
cd PETs-Applications/homomorphic_encryption/criminal_data_cloud_computing/node.js
mkdir uploads/
cp ../tfhe-police/build/server uploads
```

#### Step 2.  Install the dependencies
```
sudo apt install nodejs
sudo apt install npm
npm install
```

#### Step 3.  Start the service
```
node TTC.js
```

### Upload The Dataset And Use The Web Service

#### Step 1. Generate private and public keys

Generate the private key(`myKey`), the associated public keys(`rfKey` and `ksKey`), and the public parameters(`CC`).

```
cd ../tfhe-police/build
./client -k
```

<img src="https://i.imgur.com/Gn9mlRK.png" width="800"/>

#### Step 2. Encrypt the dataset

Encrypt the dataset and output the result as `encData.zip`.
```
./client -e encData
```

<img src="https://i.imgur.com/fliMyTk.png" width="800"/>

#### Step 3. Prepare the encrypted name data, `cts.zip`

For example, if we want to search for Bryan in the dataset:
```
./client -n Bryan
```

<img src="https://i.imgur.com/fpQDPE4.png" width="800"/>

#### Step 4. Upload files to the webpage

Connect to the webpage with a browser and upload the files accordingly.

<img src="https://i.imgur.com/vN4Sgbx.png" width="800"/>

#### Step 5. Choose the function `query` or `count` on the webpage

+ Use `query` to find the data corresponding to the specific name.

<img src="https://i.imgur.com/9IziaxU.png" width="800"/>

+ Use `count` to count the number of the specific names appearing in the dataset. 

<img src="https://i.imgur.com/aD1hOWe.png" width="800"/>


#### Step 6. Click `UPLOAD & RUN`

Click the `UPLOAD & RUN` button to start.

<img src="https://i.imgur.com/WHkycoW.png" width="800"/>

Once a dialog pops up, the process successfully finishes.

<img src="https://i.imgur.com/KMWIzwu.png" width="800"/>

<img src="https://i.imgur.com/vbwgRsB.png" width="800"/>


#### Step 7. Decrypt the returned result

Click `DOWNLOAD` to download the result and move it to your working directory.

<img src="https://i.imgur.com/BDkJxs7.png" width="800"/>

If you choose the `query` function, decrypt the result with:
```
./client -d queryData
```

<img src="https://i.imgur.com/bsSxXPU.png" width="800"/>


Otherwise, if you choose the `count` function, decrypt the result with:
```
./client -c countResult
```

<img src="https://i.imgur.com/RpyNvDy.png" width="800"/>

## Disclaimer

The application listed here only serves as the minimum demonstration of using PETs. The source code should not be directly deployed for production use.
