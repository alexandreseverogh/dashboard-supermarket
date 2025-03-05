import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_scripts=external_stylesheets)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Label("Dropdown"),

    dcc.Dropdown(
        id="dp-1",
        options=[
        {'label': 'Piauí', 'value': 'PI'},
        {'label': 'Maranhão', 'value': 'MA'},
        {'label': 'Ceará', 'value': 'CE'},
        {'label': 'Rio Grande do Norte', 'value': 'RN'},
        {'label': 'Paraíba', 'value': 'PB'},
        {'label': 'Pernambuco', 'value': 'PE'},
        {'label': 'Alagoas', 'value': 'AL'},
        {'label': 'Sergipe', 'value': 'SE'},
        {'label': 'Bahia', 'value': 'BA'}],
        value="PE",style={"margin-bottom": "25px"}
    ),

    html.Label("Checklist"),
    dcc.Checklist(
        id="cl-1",
        options=[
        {'label': 'Piauí', 'value': 'PI'},
        {'label': 'Maranhão', 'value': 'MA'},
        {'label': 'Ceará', 'value': 'CE'},
        {'label': 'Rio Grande do Norte', 'value': 'RN'},
        {'label': 'Paraíba', 'value': 'PB'},
        {'label': 'Pernambuco', 'value': 'PE'},
        {'label': 'Alagoas', 'value': 'AL'},
        {'label': 'Sergipe', 'value': 'SE'},
        {'label': 'Bahia', 'value': 'BA'}],
        value=["PE"],style={"margin-bottom": "25px"}
    ),

    html.Label("Text Input"),
    dcc.Input(value='PE', type='text'),

    html.Label("Slider"),
    dcc.Slider(
        min=0,
        max=9,
        marks= {i: 'Label {}'.format(i) if i==1 else str(i) for i in range(1, 6)},
        value=5,
    ),
])   
    
if __name__== '__main__':
    app.run_server(debug=True)