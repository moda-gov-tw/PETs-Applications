from PETWorks import PETAnonymization, output
from PETWorks.attributetypes import *

originalData = "NHANES.csv"
dataHierarchy = "NHANES_hierarchy"

attributeTypes = {
    "RIAGENDR": QUASI_IDENTIFIER,
    "RIDAGEYR": QUASI_IDENTIFIER,
    "RIDRETH1": QUASI_IDENTIFIER,
    "DMDEDUC2": QUASI_IDENTIFIER,
    "DMDMARTL": SENSITIVE_ATTRIBUTE,
    "BMXBMI": SENSITIVE_ATTRIBUTE,
    "DPQ020":SENSITIVE_ATTRIBUTE,
    "INDFMMPI":SENSITIVE_ATTRIBUTE,
    "LBXGH":SENSITIVE_ATTRIBUTE,
    "METS":SENSITIVE_ATTRIBUTE,
    "QMETS":SENSITIVE_ATTRIBUTE,
    "finflg":SENSITIVE_ATTRIBUTE
}

result = PETAnonymization(
    originalData,
    "k-anonymity",
    dataHierarchy,
    attributeTypes,
    maxSuppressionRate=0.6,
    k=6,
)

output(result, "output.csv")
