import sys
import pandas as pd
import numpy as np

'''
lecture des txt et écriture csv
'''

fn=sys.argv[1] # "data/ValeursFoncieres-2025-S1.txt"

# lecture du source, selection de colonnes
cols='Date mutation|Nature mutation|Valeur fonciere|Code postal|Commune|Surface Carrez du 1er lot|Code type local|Type local|Nombre pieces principales|Surface terrain'.split('|')
names='date|nature|valeur|cp|commune|surface|code_type|local|pieces|terrain'.split('|')
df = pd.read_csv(fn, sep='|', usecols=cols, dtype={'Valeur fonciere':np.float64, 'Code postal':str}, decimal=',')
df.columns=names

df=df[df.nature=='Vente']
df=df[~np.isnan(df.code_type)]
df.fillna(0.0, inplace=True)
print(df)
print(df.dtypes)

df.to_csv(fn+".csv")