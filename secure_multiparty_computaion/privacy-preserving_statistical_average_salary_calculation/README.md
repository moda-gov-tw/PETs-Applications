# Privacy-Preserving Statistical Average Salary Calculation

Gender wage gap refers to the disparity in earnings that arises due to gender within the same job positions or similar roles. This phenomenon is prevalent in many countries and across various industries, but the specific extent of the gap can vary based on factors such as region, industry, education level, and job position.

This case study is based on the Boston Women's Workforce Council's use of Secure Multi-Party Computation (SMPC) in 2015, 2016, 2017, 2019, and 2021 to investigate gender wage gaps among approximately one-sixth of Boston's salaried employees.

**So why not simply disclose everyone's individual salaries for the investigation?** There are several reasons for this:

1. Privacy Protection: Salary information is sensitive personal data, and unrestricted disclosure of salary details may infringe upon employees' privacy, leading to unnecessary external interference and judgment.

2. Social Comparison and Awkwardness: Directly disclosing individual salary details can lead to comparisons and unnecessary competition and friction among colleagues.

3. Complexity and Diversity: Salary structures within organizations are often highly complex, involving various factors such as different job positions, work experiences, and skill levels. Therefore, the salaries of specific individuals may not accurately reflect an organization's actual gender pay strategy. Full salary disclosure may overshadow the overall gender wage gap due to specific employees' salaries.

4. Occupational Confidentiality: Some positions may require confidentiality, involving sensitive information such as customer data and business strategies. Publicly disclosing the salary details of these positions could have adverse effects on the company's operations.

Therefore, the goal is to pursue gender pay equality while safeguarding individuals' privacy, which is why Secure Multi-Party Computation technology is used to conduct the investigation of average gender salaries.

In the following scenario, we assume that the Department of Labor intends to conduct a statistical average salary calculation using secure multi-party computation and has outsourced the task to Vendor A to assist with the execution.(for detailed descriptions of each role, please refer to [here](https://hackmd.io/@petworks/HkjnwIJHs/https%3A%2F%2Fhackmd.io%2F%40petworks%2FBJL1QwxPh#%E8%A6%8F%E6%A0%BC%E9%99%B3%E8%BF%B0))Our role assignments are as follows:

|Role | Who | Work | 
|:--------: | :--------: | :--------: |   
|Data Provider| Employee($Client_1,...,Client_n$) | Transform secret inputs into "shares" and hand them over to the computing provider for calculation. Here, we assume that each employee is assigned a pre-distributed ID (in practice, we typically integrate this into the identity authentication system, so once authentication is successful, the system can provide the employee's ID).  | 
|Stop Provider| Department of Labor($Client_0$) | Declare the end of salary collection and commence the computation.  | 
|Computing Provider| Vendor A($MPC\ node_0,...,MPC\ node_{m-1}$)  | Collect the "shares" from each data provider and use them for computation.  | 
|Result Obtainer| Vendor A($MPC\ node_0$) | Retrieve the results and share them with the other parties. | 

## Dataset
We will generate randomly simulated salary data with the following data fields:

1.  Gender: Records the gender of employees, with three options: male, female, and other.
2.  Salary （NTD/Month）: Represents the monthly salary of each employee, measured in New Taiwan Dollars (NTD).

|ID | Gender     | Salary（NTD/Month） | 
|:--------: | :--------: | :--------: |
|1| Female | 1123701  | 

|ID | Gender     | Salary（NTD/Month） | 
|:--------: | :--------: | :--------: |
|2| Male | 23222  | 

|ID | Gender     | Salary（NTD/Month） | 
|:--------: | :--------: | :--------: |
|3| Other | 321111  | 

## Used PETs

Secure Multi-Party Computation

## Goals of Using PETs

Secure Multi-Party Computation (SMPC) allows for the calculation of employees' average salaries while ensuring the privacy of individual salary information of participants in the wage survey.

## Data Processing

The fundamental operation of secure multi-Party computation (SMPC) involves participants masking their own secret inputs and subsequently collaboratively calculating a common computational goal.

In the current context, each employee is responsible for providing their salary (secret input), so they need to process their salary in a way that cannot be deciphered before handing it over to the deployed SMPC nodes for computation. The detailed process is as illustrated in the diagram below:

![](https://github.com/B08902060/secure_multiparty_computaion/blob/main/image/001.png)

In this example, we utilize secret sharing techniques to enable employees to transform their own salaries into multiple "shares." This ensures that individual MPC nodes cannot independently decipher a specific employee's salary. After a set period of time, a Stop Provider will send a termination signal to each MPC node. At this point, the MPC nodes can commence secure multi-party computation, ultimately resulting in the publication of the average salaries for each gender.

Furthermore, since MP-SPDZ uses openssl to establish a secure channel, we need to create certificates and distribute them to each MPC node, Data Providers, and the Stop Provider(Assume that this step has already been completed by default). This is done to ensure the security of the transmission.

## Quick Start
### Deployment Stage
In this stage, we will establish secure channels between the participants, using OpenSSL for this purpose. If you wish to perform testing on your own, you can use MPC_node 0 as the default to carry out the actions of this stage (create and distribute certificates).

#### Create and distribute certificates
Step 1: Clone MP-SPDZ
```
git clone https://github.com/data61/MP-SPDZ.git
cd MP-SPDZ
```
Step 2. Generate Certificate
```
./Scripts/setup-ssl.sh <the_number_of_MPC_nodes>
./Scripts/setup-clients.sh <the_number_of_Data_providers>
```
Certificates will be placed at `Player-Data/`.

Step 3. Distribute certificates  
Send `Pi.pem`,`Pi.key`(`i` is the ID of MPC nodes),`C*.pem`(all providers' `*.pem`) to each MPC node.  
Send `Ci.pem`,`Ci.key`(`i` is the ID of Data provider),`P*.pem`(all MPC nodes' `*.pem`) to each Data Provider.  
Send `C0.pem`,`C0.key`,`P*.pem`(all MPC nodes' `*.pem`) to Stop Provider.  
*** In this stage, MPC nodes are set to default, with the expectation that the vendor will handle certificate distribution during deployment. As for the data providers' part, it is practical to have a certification authority or entity to perform the distribution. ***

### Preparation Stage
#### MPC nodes
Step 1: Build and install MP-SPDZ using `make -j 8 tldr`. If you don't know how to do it, please check [MP-SPDZ documentation](https://mp-spdz.readthedocs.io/en/latest/).
```
git clone https://github.com/data61/MP-SPDZ.git
cd MP-SPDZ
make -j 8 tldr      //Rapidly construct the necessary files
make -j 8 shamir    //build the available protocol: shamir-party.x.
```
In this case, we opt for a semi-honest protocol, so we have employed the Shamir protocol. If we were to use a malicious-secure protocol (MASCOT), then the computation time in the context of three computing parties (i.e., locally) would compare as follows:
|Protocol | Time     | 
|:--------: | :--------: |
|shamir| 0.047469 |
|mascot| 7.18371 |

Step 2: Clone MPC_node
```
git clone https://github.com/moda-gov-tw/PETs-Applications.git
```
Step 3: Copy and move `average_gender_salary.mpc` to `Program/Source/`
```
cp PETs-Applications/secure_multiparty_computaion/privacy-preserving_statistical_average_salary_calculation/MPC_node/average_gender_salary.mpc Program/Source/
```
Step 4. Compile MPC file
```
./compile.py average_gender_salary.mpc
```
Step 5. Setup Certificate: receive `Pi.pem`,`Pi.key`(`i` is the ID of MPC nodes),`C*.pem`(all providers' `*.pem`); move them to `Player-Data/`; run `c_rehash <directory>` on its location.
```
mv /path/to/file/Pi.pem Player-Data/
mv /path/to/file/Pi.key Player-Data/
mv /path/to/file/C*.pem Player-Data/
c_rehash Player-Data/
```

#### Data provider
Step 1: Clone Client/Data_provider
```
git clone https://github.com/moda-gov-tw/PETs-Applications.git
cd PETs-Applications/secure_multiparty_computaion/privacy-preserving_statistical_average_salary_calculation/
```
Step 2: Install `gmpy2`
```
pip3 install gmpy2
```
Step 3. Setup Certificate: receive `Ci.pem`,`Ci.key`(`i` is the ID of Data provider),`P*.pem`(all MPC nodes' `*.pem`); move them to `Player-Data/`
```
mv /path/to/file/Ci.pem Player-Data/
mv /path/to/file/Ci.key Player-Data/
mv /path/to/file/P*.pem Player-Data/
```

#### Stop provider 
Step 1: Clone Client/Stop_provider
```
git clone https://github.com/moda-gov-tw/PETs-Applications.git
cd PETs-Applications/secure_multiparty_computaion/privacy-preserving_statistical_average_salary_calculation/
```
Step 2: Install `gmpy2`
```
pip3 install gmpy2
```
Step 3. Setup Certificate: receive `C0.pem`,`C0.key`,`P*.pem`(all MPC nodes' `*.pem`); move them to `Player-Data/`
```
mv /path/to/file/C0.pem Player-Data/
mv /path/to/file/C0.key Player-Data/
mv /path/to/file/P*.pem Player-Data/
```

### Computation Stage
Step 1. MPC nodes start MPC protocol.
```
./shamir-party.x -N <the_number_of_MPC_nodes> -p <ID_of_MPC_nodes> -h <IP_of_MPC_node_0> -pn <PortNumber_of_MPC_node_0> average_gender_salary
```
If you don't know how to do it or meet any issue, please check [MP-SPDZ documentation](https://mp-spdz.readthedocs.io/en/latest/).

Step 2. Data providers connect and sent data(secret input) to MPC nodes.
```
python3 Client/Data_provider/average_salary.py <the_number_of_MPC_node> 14000 <IP_of_MPC_node_0> ... <IP_of_MPC_node_(m-1)>
```
14000 is the listening port number of $MPC\ node_0$ (that of $MPC\ node_i$ is $14000+i$). You can adjust it in `MPC_node/average_gender_salary.mpc`

Step 3. When the time is up, Stop provider issues the command to terminate the MPC protocol.
```
python3 Client/Stop_provider/average_salary_finish.py <the_number_of_MPC_node> 14000 <IP_of_MPC_node_0> ... <IP_of_MPC_node_(m-1)>
```

Step 4. MPC node 0 will output the result.
MPC node 0 shares the result with Data providers.


## Reference


Please refer to [here](https://hackmd.io/@petworks/SyQChh9A2) for the Chinese version of this documentation. 

## Disclaimer

The application listed here only serves as the minimum demonstrations of using PETs. The source code should not be directly deployed for production use.
