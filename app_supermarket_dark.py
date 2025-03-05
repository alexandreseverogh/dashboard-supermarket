import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly.express as px
import dash_bootstrap_components as dbc

from dash_bootstrap_templates import load_figure_template

# Aplicando o tema escuro do Bootstrap
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# Carregar dados
df_data = pd.read_csv("supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data["Date"])

# ========= Layout ========= #
app.layout = html.Div(children=[
    dbc.Row([
        # Barra lateral escura
        dbc.Col([
            dbc.Card([
                html.H2("ASIMOV", style={"font-family": "Voltaire", "font-size": "35px", "color": "white"}),
                html.Hr(),
                html.H5("Cidades:", style={"color": "white"}),
                dcc.Checklist(
                    df_data["City"].value_counts().index,
                    df_data["City"].value_counts().index,
                    id="check_city",
                    inputStyle={"margin-right": "5px", "margin-left": "10px"}
                ),
                html.H5("Variável de análise:", style={"margin-top": "30px", "color": "white"}),
                dcc.RadioItems(
                    ["gross income", "Rating"], "gross income", id="main_variable",
                    inputStyle={"margin-right": "5px", "margin-left": "10px"}
                ),
            ], style={"height": "90vh", "margin": "20px", "padding": "20px", "background-color": "#1E1E1E"}, 
               color="dark", inverse=True)
        ], sm=2),

        # Área dos gráficos
        dbc.Col([
            dbc.Row([
                dbc.Col([dcc.Graph(id="city_fig")], sm=4),
                dbc.Col([dcc.Graph(id="gender_fig")], sm=4),
                dbc.Col([dcc.Graph(id="pay_fig")], sm=4)
            ]),
            dbc.Row([dcc.Graph(id="income_per_date_fig")]),
            dbc.Row([dcc.Graph(id="income_per_product_fig")]),
        ], sm=10)
    ])
])

# ========= Callbacks ========= #
@app.callback([
    Output('city_fig', 'figure'),
    Output('pay_fig', 'figure'),
    Output('gender_fig', 'figure'),
    Output('income_per_date_fig', 'figure'),
    Output('income_per_product_fig', 'figure'),
], [
    Input('check_city', 'value'),
    Input('main_variable', 'value')
])
def render_graphs(cities, main_variable):
    operation = np.sum if main_variable == "gross income" else np.mean
    df_filtered = df_data[df_data["City"].isin(cities)]
    
    df_city = df_filtered.groupby("City")[main_variable].apply(operation).reset_index()
    df_gender = df_filtered.groupby(["Gender", "City"])[main_variable].apply(operation).reset_index()
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(operation).reset_index()
    df_income_time = df_filtered.groupby("Date")[main_variable].apply(operation).reset_index()
    df_product_income = df_filtered.groupby(["Product line", "City"])[main_variable].apply(operation).reset_index()

    # Paleta de cores mais suaves
    custom_colors = ["#636EFA", "#EF553B", "#00CC96"]  # Azul escuro, Vermelho neutro, Verde menos vibrante

    # Criando os gráficos com cores mais harmoniosas
    fig_city = px.bar(df_city, x="City", y=main_variable, color="City", color_discrete_sequence=custom_colors)
    fig_payment = px.bar(df_payment, y="Payment", x=main_variable, orientation="h", color_discrete_sequence=["#636EFA"])
    fig_gender = px.bar(df_gender, y=main_variable, x="Gender", color="City", barmode="group", color_discrete_sequence=custom_colors)
    fig_product_income = px.bar(df_product_income, x=main_variable, y="Product line", color="City", orientation="h", barmode="group", color_discrete_sequence=custom_colors)
    fig_income_date = px.bar(df_income_time, y=main_variable, x="Date", color_discrete_sequence=["#636EFA"])

    # Aplicando um tema escuro uniforme para todos os gráficos
    dark_theme = {
        "plot_bgcolor": "#1E1E1E",  # Fundo interno dos gráficos escuro
        "paper_bgcolor": "#1E1E1E",  # Fundo externo escuro
        "font": {"color": "white"},  # Texto branco
    }

    for fig in [fig_city, fig_payment, fig_gender, fig_income_date, fig_product_income]:
        fig.update_layout(**dark_theme, margin=dict(l=0, r=0, t=20, b=20))

    return fig_city, fig_payment, fig_gender, fig_income_date, fig_product_income

# ========= Rodar servidor ========= #
if __name__ == "__main__":
    app.run_server(debug=True)
