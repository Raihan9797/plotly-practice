import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import plotly.graph_objects as go
import datetime

df = pd.read_csv('data/mystocks.csv')

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

line_graph = dcc.Graph(id = 'line_graph', figure = {})

line_graph_dpdn = dcc.Dropdown(
    id = 'line_graph_dpdn',
    value = ['GOOGL'],
    multi = True,
    options = [
        {'label': x, 'value': x} for x in sorted(df['Symbols'].unique())
    ]
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        line_graph_dpdn,
                        line_graph,
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    Output('line_graph', 'figure'),
    Input('line_graph_dpdn', 'value')
)
def update_graph(slct):
    dff = df.copy()
    dff = dff[dff['Symbols'].isin(slct)]

    # fig = px.line(
    #     dff,
    #     x = 'Date',
    #     y = 'Close',
    #     color = 'Symbols'
    # )

    fig = go.Figure()
    for symbol in slct:
        new_dff = dff.copy()
        new_dff = dff[dff['Symbols'] == symbol]

        fig.add_trace(
            go.Scatter(
                x = new_dff['Date'],
                y = new_dff['Close'],
            )
        )

    return fig



if __name__ == "__main__":
    app.run_server(debug = True)