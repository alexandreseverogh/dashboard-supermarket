import dash
from dash import html, dcc, Input, Output, callback_context

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Button('Button 1', id='btn-1-ctx-example'),
    html.Button('Button 2', id='btn-2-ctx-example'),
    html.Button('Button 3', id='btn-3-ctx-example'),
    html.Div(id='container-ctx-example')
])

@app.callback(Output('container-ctx-example','children'),
              Input('btn-1-ctx-example','n_clicks'),
              Input('btn-2-ctx-example','n_clicks'),
              Input('btn-3-ctx-example','n_clicks'))
def display(btn1, btn2, btn3):
    id_triggered = callback_context.triggered[0]['prop_id'].split('.')[0]
    if id_triggered == 'btn-1-ctx-example':
        print('button 1')
    if id_triggered == 'btn-2-ctx-example':
        print('button 2')
    if id_triggered == 'btn-3-ctx-example':
        print('button 3')

    return id_triggered

if __name__ == '__main__':
    app.run_server(debug=True)
