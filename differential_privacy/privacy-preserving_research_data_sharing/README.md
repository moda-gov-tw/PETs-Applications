# Shared Diabetes Prediction Research Data

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

Differential Privacy、k-anonymization、Synthetic Data

## Goals of Using PETs

To protect the information of participants involved in the NHANES data collection, measures must be taken to prevent these participants from being targeted and inferred. Additionally, the released data should retain a significant degree of usability for subsequent observation or data analysis.

## Data Processing

1. Differential Privacy

For the NHANES dataset to be released in a way to satisfy differential privacy, we must first find a way to generate the data. Noise is injected into the output of functions involving statistical computations. An intuitive approach is to convert the data distribution into a contingency table and then inject DP noise into each count value. The noisy contingency table is converted back to the releasable dataset by sampling according to the new but noisy statistical distribution. The figure below shows an overall procedure of the differentially private data synthesis. We note that the in the figure below, the post-processing techniques such as integrality, non-negativity, and consistency are also included to enhance the quality of the synthetic dataset. However, such post-processing techniques are optional.

2. k-anonymization

To release the NHANES dataset in compliance with k-anonymity, it's crucial first to determine which column in the dataset serves as the Sensitive Attribute (SA) while treating the other attributes as Quasi-identifiers (QI). Subsequently, suppression and generalization are applied to categorical attributes. The objective is to ensure that each record in the data is indistinguishably similar to at least k-1 other records within the dataset. However, a single iteration often fails to meet the above criteria because while de-identifying the data, one should preserve the usability of the original information as much as possible. Hence, the de-identification process typically adopts a progressive approach, gradually intensifying the strength of suppression and generalization (e.g., increasing the masked digits in zip codes from the last two to three digits) until the dataset meets the k-anonymity definition, after which the k-anonymized dataset is outputted.

3. Synthetic Data

To create a synthetic dataset from the NHANES dataset for release, it's crucial to first analyze the structure, distribution, and relationships within the original data. Subsequently, statistical models or machine learning techniques, such as Generative Adversarial Networks (GANs), are employed to capture the characteristics of the original data. Once the model is sufficiently trained, it can produce new data items that statistically resemble the original data but do not directly reflect any specific records from the original dataset.


## Quick Start - Differential Privacy
### Environment Prerequisites

- Ensure that your Python version is `3.7.1` or higher but below `3.11`.

### Step 1: Install `smartnoise-synth` and `openDP`

Launch your terminal and execute the following commands:
```
pip install smartnoise-synth
pip install openDP==0.6.2
```

> **Note:** Upon running `pip install openDP==0.6.2`, you might encounter an error in red text, suggesting that `smartnoise-synth` necessitates `openDP` to be of version `>= 0.7.0`. Nonetheless, due to the absence of a certain API in `openDP` versions post `0.7.0` that is vital for `smartnoise-synth`, we intentionally opt for version `0.6.2`.

### Step 2: Retrieve the Sample Code

In the terminal, execute the following command:
```
git clone https://github.com/moda-gov-tw/PETs-Applications.git
```

### Step 3: Execute the Sample Code

Navigate to the relevant directory and run the sample code with these commands:
```
cd PETs-Applications/differential_privacy/privacy-preserving_research_data_sharing
python3 example_DP.py
```

## Reference
Please refer to [here](https://hackmd.io/Wyxi11CrQpelLfnRdoCBtA) for the Chinese version of this documentation. 

## Disclaimer
The application listed here only serves as the minimum demonstration of using PETs. The source code should not be directly deployed for production use.
