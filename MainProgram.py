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
db=pd.read_csv('./raw_data/Fig1_data.csv',sep=';')


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
    data = [go.Scatter(x=db['Grade'].values,y=100*db[x].values,name=x) for x in ['2015 National','2016 National','2015 Public Schools','2016 Public Schools','2015 Private Schools','2016 Private Schools']]
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
    print(graphJSON_Fig1)
    
    
    navOptions=navOptionsMenu 
    Content=ContentMenu 
    
    
    session["Language"]=Language
                               
    return render_template('Home.html', 
                           navOptions=navOptions,  
                           Content=Content,                          
                           ButtonPressed = Language,
                           ActiveLink='/',
                           graphJSONFig1=graphJSON_Fig1)
    

if __name__=='__main__':
    #app.run(debug=True)
    app.run(debug=True,host='localhost')
