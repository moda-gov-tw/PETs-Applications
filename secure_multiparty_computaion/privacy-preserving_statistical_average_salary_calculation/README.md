# Privacy-Preserving Statistical Average Salary Calculation

Gender wage gap refers to the disparity in earnings that arises due to gender within the same job positions or similar roles. This phenomenon is prevalent in many countries and across various industries, but the specific extent of the gap can vary based on factors such as region, industry, education level, and job position.

This case study is based on the Boston Women's Workforce Council's use of Secure Multi-Party Computation (SMPC) in 2015, 2016, 2017, 2019, and 2021 to investigate gender wage gaps among approximately one-sixth of Boston's salaried employees.

**So why not simply disclose everyone's individual salaries for the investigation?** There are several reasons for this:

1. Privacy Protection: Salary information is sensitive personal data, and unrestricted disclosure of salary details may infringe upon employees' privacy, leading to unnecessary external interference and judgment.

2. Social Comparison and Awkwardness: Directly disclosing individual salary details can lead to comparisons and unnecessary competition and friction among colleagues.

3. Complexity and Diversity: Salary structures within organizations are often highly complex, involving various factors such as different job positions, work experiences, and skill levels. Therefore, the salaries of specific individuals may not accurately reflect an organization's actual gender pay strategy. Full salary disclosure may overshadow the overall gender wage gap due to specific employees' salaries.

4. Occupational Confidentiality: Some positions may require confidentiality, involving sensitive information such as customer data and business strategies. Publicly disclosing the salary details of these positions could have adverse effects on the company's operations.

Therefore, the goal is to pursue gender pay equality while safeguarding individuals' privacy, which is why Secure Multi-Party Computation technology is used to conduct the investigation of average gender salaries.


![](https://hackmd.io/_uploads/HyebvKpah.png)
[圖片來源](https://www.mdpi.com/2410-387X/4/3/25)

<p class="text-center">▲ 圖SMPC-2、安全多方運算擬真情境架構圖</p>
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

:::info
請昱維將 [擬真情境 HackMD](https://hackmd.io/tsCygT4XQsyNxlqZlsSgEQ) 的「隱私強化技術運作方式/機制說明」 譯成英文，並參考架構填充至此。
+ 以一個段落說明擬真情境內各參與角色為何
+ 列點說明資料處理的每個步驟
+ 提供 資料處理流程圖
:::

The fundamental operation of Secure Multi-Party Computation (SMPC) involves participants masking their own secret inputs and subsequently collaboratively calculating a common computational goal.

In the current context, each employee is responsible for providing their salary (secret input), so they need to process their salary in a way that cannot be deciphered before handing it over to the deployed SMPC nodes for computation. The detailed process is as illustrated in the diagram below:

![](https://hackmd.io/_uploads/HyebvKpah.png)
[圖片來源](https://www.mdpi.com/2410-387X/4/3/25)

<p class="text-center">▲ 圖SMPC-2、安全多方運算擬真情境架構圖</p>

In this example, we utilize secret sharing techniques to enable employees to transform their own salaries into multiple "shares." This ensures that individual MPC nodes cannot independently decipher a specific employee's salary. After a set period of time, a Stop Provider will send a termination signal to each MPC node. At this point, the MPC nodes can commence secure multi-party computation, ultimately resulting in the publication of the average salaries for each gender.

Furthermore, since MP-SPDZ uses openssl to establish a secure channel, during the deployment phase, we require a Coordinator(assumed by MPC Node 0) to create certificates and distribute them to each MPC node, Data Providers, and the Stop Provider. This is done to ensure the security of the transmission.

## Quick Start
### Preparation Stage
#### Coordinator
Step 1: Clone MP-SPDZ
```
git clone https://github.com/data61/MP-SPDZ.git
cd MP-SPDZ
make -j 8 tldr
```
Step 2. Generate Certificate
```
./Scripts/setup-ssl.sh <the_number_of_MPC_nodes>
./Scripts/setup-clients.sh <the_number_of_Data_providers>
```
Ｗe make MPC node 0 as the coordinator.
#### MPC nodes
Step 1: Build and install MP-SPDZ using `make -j 8 tldr`. If you don't know how to do it, please check [MP-SPDZ documentation](https://mp-spdz.readthedocs.io/en/latest/).
```
git clone https://github.com/data61/MP-SPDZ.git
cd MP-SPDZ
make -j 8 tldr
```
Step 2: Clone MPC_node

Step 3: Cope and move `average_gender_salary.mpc` to `Program/Source/`
```
cp MPC_node/average_gender_salary.mpc Program/Source/
```
Step 4. Compile MPC file
```
./compile.py average_gender_salary.mpc
```
Step 5. Setup Certificate
Receive `Pi.pem`,`Pi.key`(`i` is the ID of MPC nodes) from Coordinator ,and move them to `Player-Data/`
```
mv /path/to/file/Pi.pem Player-Data/
mv /path/to/file/Pi.key Player-Data/
```

#### Data provider
Step 1: Clone Client/Data_provider

Step 2: Install `gmpy2`
```
pip3 install gmpy2
```
Step 3. Setup Certificate <br>
Receive `Ci.pem`,`Ci.key`(`i` is the ID of Data provider) from Coordinator ,and move them to `Player-Data/`
```
mv /path/to/file/Ci.pem Player-Data/
mv /path/to/file/Ci.key Player-Data/
```

#### Stop provider 
Step 1: Clone Client/Stop_provider

Step 2: Install `gmpy2`
```
pip3 install gmpy2
```
Step 3. Setup Certificate <br>
Receive `C0.pem`,`C0.key` from Coordinator ,and move them to `Player-Data/`
```
mv /path/to/file/C0.pem Player-Data/
mv /path/to/file/C0.key Player-Data/
```


### Computation Stage
Step 1. MPC nodes start MPC protocol.
```
./mascot-party.x -N <the_number_of_MPC_nodes> -p <ID_of_MPC_nodes> -h <IP_of_MPC_node_0> average_gender_salary
```
If you don't know how to do it or meet any issue, please check [MP-SPDZ documentation](https://mp-spdz.readthedocs.io/en/latest/).

Step 2. Data providers connect and sent data(secret input) to MPC nodes.
```
python3 Client/Data_provider/average_salary.py <the_number_of_MPC_node> 14000 <IP_of_MPC_node_0> ... <IP_of_MPC_node_(m-1)>
```

Step 3. When the time is up, Stop provider issues the command to terminate the MPC protocol.
```
python3 Client/Stop_provider/average_salary_finish.py <the_number_of_MPC_node> 14000 <IP_of_MPC_node_0> ... <IP_of_MPC_node_(m-1)>
```

Step 4. MPC node 0 will output the result.



## Reference


Please refer to [here](https://hackmd.io/tsCygT4XQsyNxlqZlsSgEQ) for the Chinese version of this documentation. 

## Disclaimer

The application listed here only serves as the minimum demonstrations of using PETs. The source code should not be directly deployed for real-world use.
