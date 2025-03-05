import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Dash app com múltiplos inputs
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Carregar dataset
df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

available_indicators = df['Indicator Name'].unique()

# Layout do dashboard
app.layout = html.Div([
    # Criando um container flexível para posicionar os Dropdowns lado a lado
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '48%', 'display': 'inline-block'}),  # Definir largura e alinhar inline

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'  # Corrigido o nome do indicador
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '48%', 'display': 'inline-block'})  # Definir largura e alinhar inline

    ], style={'display': 'flex', 'justifyContent': 'space-between'}),  # Estilização do container principal

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    )
])


# Callback para atualizar o gráfico
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('year--slider', 'value')]
)
def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type, year_value):
    # Filtrar dados pelo ano selecionado
    dff = df[df['Year'] == year_value]

    # Criar subconjuntos de dados para os indicadores selecionados
    dff_x = dff[dff['Indicator Name'] == xaxis_column_name]
    dff_y = dff[dff['Indicator Name'] == yaxis_column_name]

    # Fazer merge para garantir que os mesmos países estejam em ambos os subconjuntos
    dff_merged = pd.merge(dff_x, dff_y, on=['Country Name', 'Year'], suffixes=('_x', '_y'))

    # Criar gráfico de dispersão
    fig = px.scatter(
        x=dff_merged['Value_x'],
        y=dff_merged['Value_y'],
        hover_name=dff_merged['Country Name']
    )

    # Ajustar layout e eixos
    fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
        hovermode='closest'
    )

    fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')
    fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

    return fig


# Rodar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)

