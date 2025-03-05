import dash_bootstrap_components as dbc
from dash import html
import dash

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "This is some card content that we'll reuse",
                className="card-text",
            ),
        ]
    ),
]

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card(card_content, color="primary", inverse=True, style={"height": "90vh", "margin-top": "10px", "padding-left": "50px"}),

            
        ], sm=4),
        dbc.Col([
            dbc.Row([
                dbc.Col(dbc.Card(card_content, color="info", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="info", inverse=True))
            ], style={"padding-top": "10px"}),
            dbc.Row([
                dbc.Col(dbc.Card(card_content, color="warning", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="warning", inverse=True)),
                dbc.Col(dbc.Card(card_content, color="warning", inverse=True))
            ], style={"padding-top": "10px"})
        ]),
    ]),

])

if __name__ == '__main__':
    app.run_server(port=8051, debug=True)