from flask import Flask, render_template, request, session
import pandas as pd
# plots
import plotly
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.express as px
import json

from scripts.import_data import df_Navbar, df_Content, db_fig1, db_fig2, db_fig3, db_fig5

KEY = '09ffd4f2e3095ee986f2adfb497bd952'

# creating app
app = Flask(__name__)
app.secret_key = KEY 

# home
@app.route('/', methods=["GET", "POST"])
def Home():

    # language
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
    data = ff.create_distplot([c['Spanish Comprehension'] for c in db_fig3], ['Non-Spanish Mother Tongue','Spanish Mother Tongue'], bin_size=.1,curve_type='normal')
    fig3 = go.Figure(data=data, layout=[])
    fig3.update_layout(title_text='Figure 3: Histogram of The Expected Value of Spanish Comprehension<br>by Self-Reported Mother tongue')
    graphJSON_Fig3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    
    # ploting Figure 4
    data = ff.create_distplot([c['Family Resources'] for c in db_fig3], ['Non Spanish Mother Tongue','Spanish Mother Tongue'], bin_size=.1,curve_type='normal')
    fig4 = go.Figure(data=data, layout=[])
    fig4.update_layout(title_text='Figure 4: Histogram of The Expected Value of Family Resources by Self-Reported Mother tongue')
    graphJSON_Fig4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    
    # plotting ploting figure 5
    fig5 = px.bar(db_fig5, x='Last Grade Reached', y='Mean Value', color='variable', 
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
