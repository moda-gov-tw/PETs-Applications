# Criminal Data Cloud Computing

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



### compile the server and client executable file
step 1: 
Build and install OpenFHE using “make install”. If you don't know how to do it, please check
[OpenFHE documentation](https://openfhe-development.readthedocs.io/en/latest/sphinx_rsts/intro/installation/linux.html).

step 2:
Clone tfhe-police.   

step 3: 
Create the build directory from the root directory of this repo, and cd to it.
```
mkdir build
cd build
```
step 4: 
Run
```
cmake ..
```

step 5: 
Run “make” to build the executable.
```
make
```

### using the network service
step 1: Compile the server file from the repo above. 

step 2: Clone node.js.  

step 3: Put the server into the uploads folder (in the current directory).
```
cd node.js
mkdir uploads/
```
step 4: install nodejs and related application
``` 
sudo apt install -y nodejs
sudo apt install npm
npm install
node TTC.js
```

## Reference


Please refer to [here](https://hackmd.io/@petworks/ByAmydrP3) for the Chinese version of this documentation. 

## Disclaimer

The application listed here only serves as the minimum demonstrations of using PETs. The source code should not be directly deployed for production use.
