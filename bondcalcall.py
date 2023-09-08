# %%
import pandas as pd
from pprint import pprint as pp
import sys
import tempfile
# %%
file='main.csv'
#file = sys.argv[1]
tfile = tempfile.NamedTemporaryFile().name
# %%
with open(file, 'r') as fin:
    data = fin.read().splitlines(True)

data = data[1:]
data = data[:-1]

with open(tfile, 'w') as fout:
    fout.writelines(data)

# %%
dfira = pd.read_csv(tfile)
#print(dfira.to_string())
#pp(dfira, width=800)
# %%
dfira['Gains']=dfira['Quantity'].replace('[\$,]', '', regex=True).astype(float)+(dfira['Amount'].replace('[\$,]', '', regex=True).astype(float))
print(dfira.to_string())
# %%
# 
dfira['TDateNt'] = None
#dfira['TDateNt']=dfira['Description'].str.extract(r'(NOTE DUE )(.*23$)')[1]

#dfira['TDateNt']=dfira['Description'].str.extract(r'(NOTE DUE )(\d\d/\d\d/\d\d$)')[1]
dfira.loc[dfira['TDateNt'].isnull(),'TDateNt'] = dfira['Description'].str.extract(r'(NOTE DUE )(\d\d/\d\d/\d\d$)')[1]
dfira.loc[dfira['TDateNt'].isnull(),'TDateNt'] = dfira['Description'].str.extract(r'(BILL DUE )(\d\d/\d\d/\d\d$)')[1]
dfira.loc[dfira['TDateNt'].isnull(),'TDateNt'] = dfira['Description'].str.extract(r'(FDIC INS DUE )(\d\d/\d\d/\d\d)(.*$)')[1]
dfira['TDateNt'] = pd.to_datetime(dfira['TDateNt'],format='%m/%d/%y')
print(dfira.to_string())
# %%

# ira account gains
dfbuyira=dfira.query('Description.str.contains("US TREASUR") and Action=="Buy" and not TDateNt.isnull()')
dfbuynotes=dfira.query('(Description.str.contains("NOTE DUE") or Description.str.contains("FDIC INS DUE") or Description.str.contains("BILL DUE")) and Action=="Buy"')
dfbuynotes['TDateNt'] = pd.to_datetime(dfbuynotes['TDateNt'],format='%m/%d/%y')
#pp(dfbuyira, width=800)

# %%
# ira total gains
#print("%.2f" % dfbuyira['Gains'].sum())
# note total gains
print("%.2f" % dfbuynotes['Gains'].sum())



# %%
# sort by maturity
dfbuynotes = dfbuynotes.sort_values(by=['TDateNt'])
print(dfbuynotes.to_string())


# %%
dfrecent = dfbuynotes[dfbuynotes['TDateNt'] > pd.Timestamp.now()]
print(dfrecent.to_string())
# %%
mindate=pd.Timestamp.now()
maxdate=dfrecent['TDateNt'].max()
index=pd.date_range(mindate, maxdate)
#results = [part for _, part in dfrecent.groupby(pd.Grouper(freq='10D'))]

# %%
dfx = dfrecent.copy()
dfx['index']=range(1,len(dfx)+1)
print(dfx.to_string())
# %%
# test data
index = pd.date_range('2021-01-01', '2021-05-01')
df = pd.DataFrame({'a': range(len(index))}, index=index)
#print(df.to_string())

#results = [part for _, part in df.groupby(pd.Grouper(freq='10D'))]

#df['date'] = df['TDateNt'].apply(lambda x: x.date()) # make date
dfs = [dfx[dfx['TDateNt'] == date] for date in dfx['TDateNt'].unique()] # group by date

def chunks(L, n): return [L[x: x+n] for x in range(0, len(L), n)]
print(type(dfs))
print(type(dfx))
print(dfs)
# %%
