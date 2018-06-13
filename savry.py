import os,sys
import pandas as pd
import seaborn as sns
import sys
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.ticker as ticker
#from matplotlib import colors
#from matplotlib.ticker import PercentFormatter

dirname = os.path.dirname(os.path.abspath(__file__))
fname = "reincidenciaJusticiaMenors.csv"
assert os.path.isfile(os.path.join('dat', fname)), "data file cannot be found"
#import data
df = pd.read_csv(os.path.join('dat', fname),low_memory=False)

#time frame of the data
print([np.min(df.V22_data_fet), np.max(df.V22_data_fet)])
#This suggests, that crimes were committed between April 2005 and October 2009. Then, there were two follow ups, one in 2013 and the other in 2015 about recidivism status.

df = df.rename(index=str, columns={"V2_estranger": "foreigner", "V1_sexe": "sex","V60_SAVRY_total_score": "full_score", \
                                  "V115_reincidencia_2015":'recid', "V4_nacionalitat_agrupat":"national_group", \
                                  "V5_edat_fet_agrupat":"age_group","V6_provincia":"province","V9_edat_final_programa": \
                                  "age_final", "V11_antecedents":"prior_crime", "V12_nombre_ante_agrupat": \
                                   "prior_crimerec","V13_nombre_fets_agrupat": "prior_crimes", "V15_fet_agrupat": \
                                  "crime_maincat", "V16_fet_violencia": "crime_violence", "V17_fet_tipus":"crime_type" \
                                  })
df['label_value'] = df.recid == 'Sí'
dfaequi=df[['id','label_value','full_score','foreigner','sex','national_group','age_group','province','age_final', \
            'prior_crime','prior_crimerec','prior_crimes','crime_maincat','crime_violence', 'crime_type' ]]


dfaequi = dfaequi[np.isfinite(dfaequi['full_score'])]
dfaequi = dfaequi.loc[dfaequi['full_score']!=99]
df = dfaequi
del dfaequi

##Value counts
N=len(df)
df.sex.value_counts() #747 male, 108 female
df['male'] = df['sex'] == 'Home'
print(df.foreigner.value_counts()) #524 spanish, 331 foreigner
df['spanish'] = df['foreigner'] == 'Espanyol'
N_sexm = df.loc[df.male==1].sum()
N_sexf = df.loc[df.male==0].sum()
N_foreign0 = df.loc[df.spanish==1].sum()
N_foreign1 = df.loc[df.spanish==0].sum()


#VERY IMPORTANT Reduce score to a binary variable
df['score']=df['full_score']>=20
df.score.value_counts()

df = df.rename(index=str, columns={"id": "entity_id","age_group": "age_cat","foreigner": "race"})