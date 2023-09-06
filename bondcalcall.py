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
#print(dfira.to_string())
# %%
# 
dfira['TDate']=dfira['Description'].str.extract(r'(US TREASURY BILL23U S T BILL DUE )(.*)')[1]
#dfira['TDateNt']=dfira['Description'].str.extract(r'(NOTE DUE )(.*23$)')[1]
dfira['TDateNt']=dfira['Description'].str.extract(r'(NOTE DUE )(\d\d/\d\d/\d\d$)')[1]
#dfira['TDateNt']=dfira['Description'].str.extract(r'(FDIC INS DUE )(\d\d/\d\d/\d\d)(.*$)')[1]
#dfira['TDateNt']=dfira['Description'].str.extract(r'(FDIC INS DUE )(\d\d/\d\d/\d\d)(.*$)|(NOTE DUE )(\d\d/\d\d/\d\d$)')[1]
dfira['TDateNt'] = pd.to_datetime(dfira['TDateNt'],format='%m/%d/%y')
print(dfira.to_string())
#pp(dfira, width=800)
# %%

# ira account gains
dfbuyira=dfira.query('Description.str.contains("US TREASUR") and Action=="Buy" and not (TDate.isnull() and TDateNt.isnull())')
dfbuynotes=dfira.query('Description.str.contains("NOTE DUE") or Description.str.contains("FDIC INS DUE") and Action=="Buy"')
print(dfbuynotes.to_string()) 
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
