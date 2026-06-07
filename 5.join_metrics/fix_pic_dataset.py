import pandas as pd

system = 'commons-bcel'
df = pd.read_csv('results2/' + system + '-perf-diff-all2.csv')
print(df['will_change'].value_counts(dropna=False))
print(df['perf_change'].value_counts(dropna=False))
# df['will_change'] = df['perf_change']
# print(df['will_change'].value_counts(dropna=False))
# print(df['perf_change'].value_counts(dropna=False))
# df.to_csv('results2/' + system + '-perf-diff-all.csv')

# df_valid = df.loc[(df['will_change'] == 1) & (df['perf_change'] == 1)]
# print(df_valid['will_change'].value_counts(dropna=False))

df_will_change = df.loc[(df['will_change'] == 1)]
print(df_will_change['will_change'].value_counts(dropna=False))

df_invalid = df.loc[(df['will_change'] == 0) & (df['perf_change'] == 1)]
print(df_invalid['will_change'].value_counts(dropna=False))


for i, row in df_invalid.iterrows():
    ifor_val = something
    if <condition>:
        ifor_val = something_else
    df.at[i,'ifor'] = ifor_val
