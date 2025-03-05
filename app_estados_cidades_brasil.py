from dash import Dash, dcc, html, Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

all_options = {
    'Brasil': [
        {'NO': [{'Amazonas': 'Manaus'}, {'Rondonia': 'Porto Velho'}, {'Acre': 'Rio Branco'}]}, 
        {'NE': [{'Pará': 'Belém'}, {'Maranhão': 'São Luís'}, {'Piauí': 'Teresina'},{'Ceará': 'Fortaleza'},{'Rio Grande do Norte': 'Natal'}, {'Paraíba': 'João Pessoa'},{'Pernambuco': 'Recife'},{'Alagoas': 'Maceió'},{'Sergipe': 'Aracaju'},{'Bahia': 'Salvador'}]}, 
        {'CO': [{'Distrito Federal': 'Brasília'}, {'Goiás': 'Goiânia'}, {'Tocantins': 'Palmas'}]}, 
        {'SE': [{'Espírito Santo': 'Vitória'}, {'Rio de Janeiro': 'Rio de Janeiro'}, {'São Paulo': 'São Paulo'},{'Minas Gerais': 'Belo Horizonte'}]}, 
        {'SU': [{'Paraná': 'Curitiba'}, {'Santa Catarina': 'Florianópolis'}, {'Rio Grande do Sul': 'Porto Alegre'}]}
    ],
    'Uruguai': [
        {'Região U1': [{'E1-RU1': 'C-E1-RU1'}, {'E2-RU1': 'C-E2-RU1'}, {'E3-RU1': 'C-E3-RU1'}]}, 
        {'Região U2': [{'E1-RU2': 'C-E1-RU2'}, {'E2-RU2': 'C-E2-RU2'}, {'E3-RU2': 'C-E3-RU2'}]}
    ]
}

app.layout = html.Div([
    dcc.RadioItems(
        list(all_options.keys()),
        'Brasil',
        id='countries-radio',
    ),
    html.Hr(),
    dcc.RadioItems(id='regioes-radio'),
    html.Hr(),
    dcc.RadioItems(id='estados-radio'),
    html.Hr(),
    html.Div(id='display-selected-capitais-values'),
])

@app.callback(
    Output('regioes-radio', 'options'),
    Input('countries-radio', 'value')
)
def set_regioes_options(selected_country):
    return [{'label': list(region.keys())[0], 'value': list(region.keys())[0]} for region in all_options[selected_country]]

@app.callback(
    Output('regioes-radio', 'value'),
    Input('regioes-radio', 'options')
)
def set_regioes_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('estados-radio', 'options'),
    Input('countries-radio', 'value'),
    Input('regioes-radio', 'value')
)
def set_estados_options(selected_country, selected_region):
    for region in all_options[selected_country]:
        if selected_region in region:
            return [{'label': list(state.keys())[0], 'value': list(state.keys())[0]} for state in region[selected_region]]
    return []

@app.callback(
    Output('estados-radio', 'value'),
    Input('estados-radio', 'options')
)
def set_estados_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('display-selected-capitais-values', 'children'),
    Input('countries-radio', 'value'),
    Input('regioes-radio', 'value'),
    Input('estados-radio', 'value')
)
def display_selected_capital(selected_country, selected_region, selected_state):
    for region in all_options[selected_country]:
        if selected_region in region:
            for state in region[selected_region]:
                if selected_state in state:
                    return f'{selected_state} ({selected_region}) - Capital: {state[selected_state]}'
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)
