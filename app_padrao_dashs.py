# ================ Estrutura Padrão de Projetos de Dashboards =======#

import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__)

server = app.server

# ========================= Layout =====================#

app.layout = html.Div(children=[

])

# ======================== Call Backs ==================#


# ======================== Run Sever ===================#

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)