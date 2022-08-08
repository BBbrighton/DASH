#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os 
import pandas as pd 
import glob 
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
pd.set_option('display.max_columns', None)


# In[2]:


parent_dir = r'C:\Users\72529rch\Dropbox (Erasmus Universiteit Rotterdam)\youngfirm_jobbkk\data\dashboard'
parent_dir_mac_os = '/Users/brighton/Dropbox (Erasmus Universiteit Rotterdam)/youngfirm_jobbkk/data/dashboard'


# In[3]:


os.chdir(parent_dir_mac_os )


# In[4]:


dat = pd.read_csv('for_plotly_dash.csv').iloc[:,1:]


# In[5]:


import plotly.io as pio
pio.renderers.default = 'iframe'


# In[6]:


dat.head()


# In[7]:


datly = dat.copy()


# In[8]:


#region_to_loop = list(dat['region'].unique()) 
region_to_loop  = datly['Region'].unique().tolist()
indus_to_loop = datly['Industry'].unique().tolist()
year_to_loop = datly['Year Start'].unique().tolist()
cap_list = datly['Capital'].unique().tolist()


# In[9]:


import plotly.express as px
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
from dash import Input, Output
# Load Data
datly = dat.copy()


# Build App
app = JupyterDash(__name__)
app.layout = html.Div([   
    
    
     html.H1(
        children='Survival Rate of Young Firms'
      ),
    
    html.Div([

        html.Div([html.Label ('Year Born'),
                
                dcc.Dropdown(
                
                id='year',
                options=[{'label': i, 'value': i} for i in year_to_loop],
                value='Year',
                placeholder="Select Year Born"
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label ('Starting Capital'),
            dcc.Dropdown(
                
                id='cap',
                options=[{'label': c, 'value': c} for c in cap_list],
                value='Registered Capital',
                placeholder="Select Starting Capital"
            ),
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}) ,
        
        html.Div([html.Label ('Region'),
            dcc.Dropdown(
                
                id='region',
                options=[{'label': c, 'value': c} for c in region_to_loop],
                value='Region',
                placeholder="Select Region"
            ),
        ], style={'width': '48%', 'float': 'bottom', 'display': 'inline-block'}),
        
        html.Div([html.Label ('Industry'),
            dcc.Dropdown(
                id='industry',
                options=[{'label': ind, 'value': ind} for ind in indus_to_loop],
                value='Industry',
                placeholder="Select Industry"
            ),
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}) 
        
        
    ]),
    

    dcc.Graph(id='graph'),

])



# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input("year", "value")],
    [Input("cap", "value")],
    [Input("region", "value")],
    [Input("industry", "value")]
)
def update_figure(year,cap,region,indus):
    fig=go.Figure( layout_yaxis_range=[20,100] , 
                   layout_xaxis_range=[0,14] ,
                   )
    fig.add_trace(go.Scatter(x=datly[(datly['Year Start'] == year) 
                                 & (datly['Industry'] == indus) 
                                 & (datly['Region'] == region)
                                 & (datly['Capital'] == cap)]['Years In Business'], 
                         y= datly[(datly['Year Start'] == year) 
                                 & (datly['Industry'] == indus) 
                                 & (datly['Region'] == region)
                                 & (datly['Capital'] == cap)]['percent'].round(2), 
                         line={},
                         visible = True
                        ))
    fig.add_annotation(
        text = (f"@brighton <br>Source: DBD calculated by the author")
        , showarrow=False
        , x = 0
        , y = -0.15
        , xref='paper'
        , yref='paper' 
        , xanchor='left'
        , yanchor='bottom'
        , xshift=-1
        , yshift=-5
        , font=dict(size=10, color="grey")
        , align="left"
        ,)
    
    fig.update_layout(template='simple_white',
                     xaxis_title="Year in Business",
                     yaxis_title="% Firms still in Business")

    return fig



# Run app and display result inline in the notebook
app.run_server(mode='inline')


# In[10]:


### Add default 
### fix styling 
### add axis name -- DONE
### add annotation for ease of reading. 
#### add text on where to find this informaiton easily. 

