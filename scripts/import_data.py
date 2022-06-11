import pandas as pd
import os


# Menu
path_to_translations = os.path.join('static','translations')
df_Navbar = pd.read_csv(os.path.join(path_to_translations,'Navbar.csv'))
df_Content = pd.read_csv(os.path.join(path_to_translations,'Content.csv'))

KEY = '09ffd4f2e3095ee986f2adfb497bd952'

# Figure 1
# uploading data
db_fig1=pd.read_csv('./raw_data/Fig1_data.csv',sep=';')

# Figure 2
# uploading data
db_fig2=pd.read_csv('./raw_data/Fig2_data.csv',sep=';')

# Figure 3 and 4
# uploading data
db_fig3=pd.read_csv('./raw_data/FactorModel_P4_HG_8_E_Latents.csv',sep=',')
db_fig32=pd.read_csv('./raw_data/DBEstimationFromFactors.csv',sep=',')
# cleaning data
db_fig32=db_fig32[['Cod_Personal','nsmt']]
db_fig3=db_fig3.merge(db_fig32,how='left',left_on='Cod_Personal',right_on='Cod_Personal')
db_nsmt=db_fig3[db_fig3['nsmt']==1]
db_smt=db_fig3[db_fig3['nsmt']==0]
db_fig3=[db_nsmt,db_smt]

# Figure 5
db_fig4=pd.read_csv('./raw_data/FactorModel_P4_HG_8_E_Latents.csv',sep=',')
db_fig42=pd.read_csv('./raw_data/DBEstimationFromFactors.csv',sep=',')
db_fig42=db_fig42[['Cod_Personal','nsmt','Cod_Estab_id']]
db_fig4=db_fig4.merge(db_fig42,how='left',left_on='Cod_Personal',right_on='Cod_Personal')
db_fig43=pd.read_csv('./raw_data/PermanenciaNotasE2013Prueba.csv',sep=';')
db_fig43=db_fig43[['COD_PERSONAL','Last Grade']]
db_fig4=db_fig4.merge(db_fig43,how='left',left_on='Cod_Personal',right_on='COD_PERSONAL')
db_fig4['Last Grade']=db_fig4['Last Grade'].astype(str)
db_fig44=pd.read_csv('./raw_data/Latents_Effects.csv',sep=',')
db_fig44=db_fig44[['Cod_Personal','Spanish Comprehension Effect','Family Resources Effect']]
db_fig4=db_fig4.merge(db_fig44,how='left',left_on='Cod_Personal',right_on='Cod_Personal')
y=db_fig4['Family Resources'].values
db_fig4=db_fig4.groupby(['Last Grade']).agg({'Spanish Comprehension':'mean','Family Resources':'mean'})
db_fig4.reset_index(inplace=True)
db_fig4=db_fig4.melt(id_vars=['Last Grade'], value_vars=['Spanish Comprehension','Family Resources'])
db_fig4['Last Grade Reached']=db_fig4['Last Grade']
db_fig4['Mean Value']=db_fig4['value']
db_fig5 = db_fig4

