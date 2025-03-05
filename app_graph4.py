import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_scripts=external_stylesheets)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H6("Digite o valor abaixo para ver o callback em ação"),
    html.Div(["Entrada", 
              dcc.Input(id='my-input', value='Valor Inicial', type='text')]),
    html.Br(),
    html.Div(id='my-output'),
])

@app.callback(
    Output(component_id="my-output", component_property="children"), 
    [Input(component_id='my-input', component_property='value')],
)
def upadate_output_div(value):
    return "Saída: {}".format(value)

if __name__== '__main__':
    app.run_server(debug=True)