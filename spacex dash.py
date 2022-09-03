import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input,Output

#import data
spacex_df=pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
# spacex_df=pd.read_csv("C:/Users/burha/Downloads/spacex_launch_dash.csv")
# spacex_df=pd.read_csv("C:\Users\burha\Downloads\spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app=dash.Dash(__name__)

#App layout
app.layout=html.Div(children=[ html.H1('SpaceX Launch Record Dashboard',
                                style={'textAlign': 'center','color':'#503D36',
                                'font-size':40}), 
                                #Add a dropdown
                                dcc.Dropdown(id='site-dropdown', 
                                options=[{'label':'All','value':'All'},
                                        {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                        {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                        {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                        {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}],
                                        value='All',
                                        placeholder='Enter name',
                                        searchable=True),
                                html.Br(),

                                #Add a pie chart
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                #Add a slider
                                html.P('Payload range (kg)'),
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                min=0,max=10000, step=1000,
                                value=[min_payload,max_payload],
                                marks={0:'0',2500:'2500',5000:'5000',7500:'7500',10000:'10000'}
                                )),
                                html.Br(),

                                #Add a scatter plot
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),

])

@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
                Input(component_id='site-dropdown',component_property='value'))

def get_pie_chart(entered_site):
        filtered_df=spacex_df
        if entered_site=='All':
                fig=px.pie(filtered_df,values='Flight Number',names='Launch Site',
                title='Total success Lauches by site')
                return fig
        else:
                filtered_df=filtered_df.loc[filtered_df['Launch Site']==entered_site]
                fig=px.pie(filtered_df,values='Flight Number',names='class',
                title='Total success Lauches for {} site'.format(entered_site))
                return fig

@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])

def get_scatter_chart(entered_site,payload):
        filtered_df=spacex_df
        if entered_site=='All':
                filtered_df=filtered_df[(filtered_df['Payload Mass (kg)']>= payload[0]) & 
                (filtered_df['Payload Mass (kg)']<= payload[1])]
                fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class', color='Booster Version Category',
                title='Correlation with Payload and Success for all Lauch sites')
                return fig
        else:
                filtered_df=filtered_df.loc[(filtered_df['Launch Site']==entered_site) &
                 ((filtered_df['Payload Mass (kg)']>= payload[0]) & (filtered_df['Payload Mass (kg)']<= payload[1]))]
                fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class', color='Booster Version Category'
                ,title='Correlation with Payload and Success for {} Lauch site'.format(entered_site))
                return fig
if __name__=='__main__':
        app.run_server()


