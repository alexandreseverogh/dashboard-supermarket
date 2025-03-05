import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc

app = dash.Dash(
    external_stylesheets=[dbc.themes.DARKLY]
)

server =  app.server

df_data = pd.read_csv("supermarket_sales.csv")

# Correção do formato de data e hora
df_data["Date"] = pd.to_datetime(df_data["Date"])
#df_data["Time"] = pd.to_datetime(df_data["Time"])

df_data["Time"] = pd.to_datetime(df_data["Time"], format="%I:%M %p", errors='coerce').dt.time

app.layout = html.Div(children=[
#    html.H5("Cidades", style={"font-size": "30px"}),
    html.H5("Cidades"),
    dcc.Checklist(
        options=[{'label': city, 'value': city} for city in df_data["City"].value_counts().index],
        value=df_data["City"].value_counts().index.tolist(),
        id="check_city", 
        inline=True
    ),
    html.H5("Variável de análise: "),
    dcc.RadioItems(
        options=[{'label': i, 'value': i} for i in ["gross income", "Rating"]],
        value="gross income",
        id="main_variable",
        inline=True
    ),

    dcc.Graph(id='city_fig'),
    dcc.Graph(id='pay_fig'),
    dcc.Graph(id="income_per_product_fig")

])

@app.callback([
            Output('city_fig', 'figure'),
            Output('pay_fig', 'figure'),
            Output('income_per_product_fig', 'figure'),
],
            [
                Input('check_city', 'value'),
                Input('main_variable', 'value')
            ])
def render_graphs(cities, main_variable):
    #cities = ["Yangon", "Mandalay"]
    #main_variable = "gross income"

    operation = np.sum if main_variable == "gross income" else np.mean

    df_filtered = df_data[df_data["City"].isin(cities)]
    
    df_city = df_filtered.groupby("City")[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby("Payment")[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(["Product line", "City"])[main_variable].apply(operation).to_frame().reset_index()
    
    fig_city = px.bar(df_city, x="City", y=main_variable)
    fig_payment = px.bar(df_payment, y="Payment", x=main_variable, orientation="h")
    fig_product_income = px.bar(df_product_income, x=main_variable, y="Product line", color="City", orientation="h", barmode="group")

    fig_city.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200, template="plotly_dark")
    fig_payment.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200, template="plotly_dark")
    fig_product_income.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=500, template="plotly_dark")

    return fig_city, fig_payment, fig_product_income

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)