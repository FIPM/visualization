from flask import Flask, render_template, request, session
import os
import pandas as pd
# plots
import plotly
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.express as px
import json



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
dbs=[db_nsmt,db_smt]

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




# creating app
app = Flask(__name__)
app.secret_key = KEY 




  
@app.route('/', methods=["GET", "POST"])
def Home():

    if session.get("Language",None)==None:
        Language=df_Navbar.columns[2]
    else:
        Language=session.get("Language")
                    
    if request.method == "POST":
        Language = request.form.get("LanguageSelected",df_Navbar.columns[2])
    
    # Navbar
    languages_to_drop = set(list(df_Navbar.columns[2:])).difference(set([Language]))
    menu = df_Navbar.drop(columns=languages_to_drop)
    names = list(menu.columns)
    names[-1]='Language'
    menu.columns = names
    navOptionsMenu=menu.groupby('Menu').agg(lambda x: x.to_list()).to_dict('records')  
    
    # Content
    menu = df_Content.drop(columns=languages_to_drop)
    names = list(menu.columns)
    names[-1]='Language'
    menu.columns = names
    menu.set_index('Keys', inplace=True)
    ContentMenu = menu.to_dict('dict')['Language']
    
    # Figure 1
    # plotting
    data = [go.Scatter(x=db_fig1['Grade'].values,y=100*db_fig1[x].values,name=x) for x in ['2015 National','2016 National','2015 Public Schools','2016 Public Schools','2015 Private Schools','2016 Private Schools']]
    layout = go.Layout(title="Figure 1: Cohort of First Grade Students in 2015 and 2016",
                    xaxis=dict(title="Last Grade Reached",
                                tickfont=dict(size=14,
                                            color='rgb(107, 107, 107)'),
                                tickangle=-45),
                    yaxis=dict(title="Student Grade Progression (%)",
                                titlefont=dict(size=16,
                                                color='rgb(107, 107, 107)'),
                                tickfont=dict(size=14,
                                            color='rgb(107, 107, 107)')),
                    )
    fig = go.Figure(data=data, layout=layout)
    graphJSON_Fig1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    # plotting fig 2
    data = [go.Scatter(x=db_fig2['Grade'].values,y=100*db_fig2[x].values,name=x) for x in ['2011 Public Schools','2015 Public Schools','2016 Public Schools']]
    layout = go.Layout(title='Figure 2: Cohort of First Grade Students in 2011, 2015, 2016<br>(Normalized to 1 in Third Grade)',
                    xaxis=dict(title='Last Grade Reached',
                                tickfont=dict(size=14,
                                                color='rgb(107, 107, 107)'),
                                tickangle=-45),
                    yaxis=dict(title='Student Grade Progression (%)',
                                titlefont=dict(size=16,
                                                color='rgb(107, 107, 107)'),
                                tickfont=dict(size=14,
                                                color='rgb(107, 107, 107)')),
                        )

    fig2 = go.Figure(data=data, layout=layout)
    graphJSON_Fig2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    # plotting figure 3
    data1 = ff.create_distplot([c['Spanish Comprehension'] for c in dbs], ['Non-Spanish Mother Tongue','Spanish Mother Tongue'], bin_size=.1,curve_type='normal')
    fig3 = go.Figure(data=data1, layout=[])
    graphJSON_Fig3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    
    # ploting Figure 4
    data1 = ff.create_distplot([c['Family Resources'] for c in dbs], ['Non Spanish Mother Tongue','Spanish Mother Tongue'], bin_size=.1,curve_type='normal')
    fig4 = go.Figure(data=data1, layout=[])
    fig4.update_layout(title_text='Figure 4: Histogram of The Expected Value of Family Resources by Self-Reported Mother tongue')
    graphJSON_Fig4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    
    # plotting ploting figure 5
    fig5 = px.bar(db_fig4, x='Last Grade Reached', y='Mean Value', color='variable', 
            barmode='group',
             height=400,
             title="Figure 5: Third Grade Students' Spanish Comprehension and Family resources"
        )
    graphJSON_Fig5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    
    navOptions=navOptionsMenu 
    Content=ContentMenu 
    
    
    session["Language"]=Language
                               
    return render_template('Home.html', 
                           navOptions=navOptions,  
                           Content=Content,                          
                           ButtonPressed = Language,
                           ActiveLink='/',
                           graphJSONFig1=graphJSON_Fig1,
                           graphJSONFig2=graphJSON_Fig2,
                           graphJSONFig3=graphJSON_Fig3,
                           graphJSONFig4=graphJSON_Fig4,
                           graphJSONFig5=graphJSON_Fig5,
                           )
    

if __name__=='__main__':
    #app.run(debug=True)
    app.run(debug=True,host='localhost')
