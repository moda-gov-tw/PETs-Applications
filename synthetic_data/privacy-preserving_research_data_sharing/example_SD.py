from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer
import pandas as pd

data = pd.read_csv("NHANES.csv")

metadata = SingleTableMetadata()

metadata.detect_from_dataframe(data=data)

synthsizer = CTGANSynthesizer(metadata=metadata)

synthsizer.fit(data)

synthetic_data = synthsizer.sample(num_rows=3985)

synthetic_data.to_csv('output.csv',index = False)


