import pandas as pd

df = pd.read_feather('/root/projectx/briziteam/textDataComp2.feather')
print(df.sample(5))