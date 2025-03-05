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

card_style = {
    'background': '#333',
    'color': 'green',
    'padding': '20px',
    'borderRadius': '10px',
    'boxShadow': '0px 4px 10px rgba(0, 0, 0, 0.5)',
    'margin': '10px',
    'width': '30%',
    'textAlign': 'center'
}

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Label("País:"),
            dcc.RadioItems(
                list(all_options.keys()),
                'Brasil',
                id='countries-radio',
            )
        ], style=card_style),
        
        html.Div([
            html.Label("Região:"),
            dcc.RadioItems(id='regioes-radio')
        ], style=card_style),
        
        html.Div([
            html.Label("Estado:"),
            dcc.RadioItems(id='estados-radio')
        ], style=card_style)
    ], style={'display': 'flex', 'justifyContent': 'center'}),
    
    html.Hr(),
    html.Div(id='display-selected-capitais-values', style={'textAlign': 'center', 'fontSize': '18px', 'marginTop': '20px'}),
    html.Div(id='wiki-link', style={'textAlign': 'center', 'marginTop': '10px'})
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
    [Output('display-selected-capitais-values', 'children'),
     Output('wiki-link', 'children')],
    [Input('countries-radio', 'value'),
     Input('regioes-radio', 'value'),
     Input('estados-radio', 'value')]
)
def display_selected_capital(selected_country, selected_region, selected_state):
    for region in all_options[selected_country]:
        if selected_region in region:
            for state in region[selected_region]:
                if selected_state in state:
                    capital = state[selected_state]
                    wiki_url = f"https://pt.wikipedia.org/wiki/{capital.replace(' ', '_')}"
                    return (f'{selected_state} ({selected_region}) - Capital: {capital}',
                            html.Div([
                                html.Label("Fontes Wikipedia:", style={'color': 'white'}),
                                html.A("Link para Wikipedia", href=wiki_url, target="_blank", style={'color': 'lightblue'})
                            ]))
    return ('', '')

if __name__ == '__main__':
    app.run_server(debug=True)



