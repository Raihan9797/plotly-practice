import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import plotly.graph_objects as go
import datetime

df = pd.read_csv('mystocks.csv')

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

bar_graph = dcc.Graph(id = 'bar_graph', figure = {})

bar_graph_checklist = dcc.Checklist(
    id = 'bar_graph_checklist',
    value = ['GOOGL'],
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
                        bar_graph_checklist,
                        bar_graph
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    Output('bar_graph', 'figure'),
    Input('bar_graph_checklist', 'value')
)
def update_graph(slct):
    dff = df.copy()
    dff = dff[dff['Symbols'].isin(slct)]
    # dff = dff.groupby(['Symbols']).mean()
    dff = dff[dff['Date'] == '2020-12-03']

    # fig = px.bar(
    #     dff,
    #     x = 'Symbols',
    #     y = 'Close'
    # )

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x = dff['Symbols'],
            y = dff['Close'],
        )
    )
    return fig



if __name__ == "__main__":
    app.run_server(debug = True)