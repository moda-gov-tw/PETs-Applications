import pandas as pd
from snsynth import Synthesizer

pums = pd.read_csv("NHANES.csv")
synth = Synthesizer.create("mwem", epsilon=1.0, split_factor=3, verbose=True)
synth.fit(pums, preprocessor_eps=0.5)
pums_synth = synth.sample(3985)

print(pums_synth)

pums_synth.to_csv('mwem_output.csv',index=False)

