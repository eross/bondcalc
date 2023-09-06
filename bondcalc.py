# %%
import pandas as pd
from pprint import pprint as pp
import sys
import tempfile
# %%
#file='linda.csv'
file = sys.argv[1]
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

# %%
dfira['Gains']=dfira['Quantity'].replace('[\$,]', '', regex=True).astype(float)+(dfira['Amount'].replace('[\$,]', '', regex=True).astype(float))

# %%
dfira['TDate']=dfira['Description'].str.extract(r'(US TREASURY BILL23U S T BILL DUE )(.*)')[1]
dfira['TDateNt']=dfira['Description'].str.extract(r'(NOTE DUE )(.*23$)')[1]

# ira account gains
dfbuyira=dfira.query('Description.str.contains("US TREASUR") and Action=="Buy" and not (TDate.isnull() and TDateNt.isnull())')
pp(dfbuyira, width=800)

# %%
# ira total gains
print("%.2f" % dfbuyira['Gains'].sum())



# %%
