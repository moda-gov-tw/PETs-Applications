# Shared Diabetes Prediction Research Data

> :exclamation: Please refer [here](https://hackmd.io/Wyxi11CrQpelLfnRdoCBtA) for the Chinese version of the scenario description.

In this case, we have two roles, which are a data owner and multiple data analysts. The data owner (e.g., NIH) is in possession of a sensitive dataset (e.g., diabetes dataset). The analysts are all interested in the diabetes dataset. Unfortunately, the sensitive dataset cannot be released directly due to privacy concerns. Thus, a common goal shared by the data owner and data analysts is to have a surrogate dataset such that the diabetes dataset will not be leaked but the analysts can still derive some statistics or build up machine learning models. 

## Dataset

The National Health and Nutrition Examination Survey (NHANES I) was initiated in 1971-1974, surveying 23,808 U.S. civilians aged 1-74. In 1981, a follow-up was begun to evaluate coronary heart disease risk factors in the U.S. The major risk factors from earlier Framingham studies were confirmed relevant for the U.S. white adult population. By 1986, the surviving NHANES I cohort (around 12,500) was re-contacted. The NHLBI funded subsequent NHANES phases. NHANES III, beginning in 1988, incorporated new features like long-term specimen banking and oversampling of Blacks and Hispanics. This series evaluated heart, vascular, lung, and blood diseases, comparing results with studies like CARDIA and the Framingham Heart Study to gauge their national representativeness. Data collection for NHANES III had two waves from 1989-1994. In 2005-2006, with cooperation from NIAID and NIEHS, an allergy component was added to NHANES to understand asthma and the impact of indoor allergens and endotoxin on allergic diseases. Objectives included estimating nationwide allergen exposure, allergic sensitization prevalence, and prevalence of major allergic diseases. The component measures allergen-specific immunoglobulin E, collects dust samples for allergen analysis, and includes added questionnaires. NHANES offers a unique database, capturing both environmental and clinical data, aiding research on links like diet, obesity, and genetics in allergic disease development.

1. gen: Gender, Male, Female.
2. age: [20, 80].
3. race: Black, Hispanic, Mexican, White, Other.
4. edu: Education level, 9th, 11th, HighSchool, College, Graduate.
5. mar: Married, Widowed, Divorced, Separated, Never, Partner.
6. bmi: Depression Yes(1), No(0).
7. pir: Poverty, Yes(1), No(0).
8. mets: Metabolic Equivalent Scores (METs) the unit is minute/week.
9. qm: Q1, Q2, Q3, Q4.
10. dia: Yes(1), No(0).

![](https://hackmd.io/_uploads/H1-hhkhbT.png)


## Used PETs

k-anonymization

## Goals of Using PETs

To protect the information of participants involved in the NHANES data collection, measures must be taken to prevent these participants from being targeted and inferred. Additionally, the released data should retain a significant degree of usability for subsequent observation or data analysis.

## Data Processing

To release the NHANES dataset in compliance with k-anonymity, it's crucial first to determine which column in the dataset serves as the Sensitive Attribute (SA) while treating the other attributes as Quasi-identifiers (QI). Subsequently, suppression and generalization are applied to categorical attributes. The objective is to ensure that each record in the data is indistinguishably similar to at least k-1 other records within the dataset. However, a single iteration often fails to meet the above criteria because while de-identifying the data, one should preserve the usability of the original information as much as possible. Hence, the de-identification process typically adopts a progressive approach, gradually intensifying the strength of suppression and generalization (e.g., increasing the masked digits in zip codes from the last two to three digits) until the dataset meets the k-anonymity definition, after which the k-anonymized dataset is outputted.

## Quick Start

The application has been tested using Python 3.9.6 on MacOS Sonoma 14.1.2 with M2 CPU and 16 GB memory.

#### Step 1. Install dependencies


Install [PETWorks-framework](https://github.com/moda-gov-tw/PETWorks-framework) by using the following command.

```
git clone https://github.com/moda-gov-tw/PETWorks-framework.git
mkdir -p PETWorks-framework/arx/lib
wget https://github.com/arx-deidentifier/arx/releases/download/v3.9.0/libarx-3.9.0.jar -P "PETWorks-framework/arx/lib/"
pip install -r PETWorks-framework/requirements.txt
```

#### Step 2. Clone the application

Clone the repository.
```
git clone https://github.com/moda-gov-tw/PETs-Applications
```

Copy the application files (including `example_k.py`, `NHANES_hierarchy`, and `NHANES.csv`) to `PETWorks-framework`. Then, go to `PETWorks-framework`.
```
cp -r PETs-Applications/k-anonymization/privacy-preserving_research_data_sharing/* PETWorks-framework
cd PETWorks-framework
```

#### Step 3. Run the application

Run the following script to process the original data, `NHANES.csv`, with k-anonymization. The output will be stored in `result.csv`.

```
python3 example_k.py
```

## Disclaimer
The application listed here only serves as the minimum demonstration of using PETs. The source code should not be directly deployed for production use.
