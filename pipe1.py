import sys
import pandas as pd
import numpy as np

'''
lecture des txt et écriture csv
'''

fn=sys.argv[1] # "data/ValeursFoncieres-2025-S1.txt"

# lecture du source, selection de colonnes
cols='Date mutation|Nature mutation|Valeur fonciere|No voie|Type de voie|Voie|Code postal|Commune|Surface Carrez du 1er lot|Surface Carrez du 2eme lot|Surface Carrez du 3eme lot|Surface Carrez du 4eme lot|Surface Carrez du 5eme lot|Code type local|Type local|Nombre pieces principales|Surface terrain'.split('|')
names='date|nature|valeur|no_voie|type_voie|voie|cp|commune|surface1|surface2|surface3|surface4|surface5|code_type|local|pieces|terrain'.split('|')
df = pd.read_csv(fn, sep='|', usecols=cols, dtype={'Date mutation':str, 'Valeur fonciere':np.float64, 'Code postal':str}, decimal=',')
df.columns=names

df=df[df.nature=='Vente'] # ne garde que les ventes
df=df[~np.isnan(df.code_type)] # ne garde que les typa 1/2/3/4
df.fillna(0.0, inplace=True) # remplis avec zéro
df.drop_duplicates(subset=['date', 'no_voie', 'type_voie', 'voie', 'cp'], keep=False, inplace=True)
df['surface_total']=df.surface1+df.surface2+df.surface3+df.surface4+df.surface5
df['prixm2']=df.valeur/df.surface_total


print(df)
print(df.dtypes)

df.to_csv(fn+".csv")