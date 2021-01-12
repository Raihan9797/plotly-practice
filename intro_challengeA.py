# challenge A: plot bar chart
# x - states, y - % of bee colonies



import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
# import plotly.graph_objects as go

# ----------------- start the app
app = dash.Dash(__name__)


# ----------------- get and clean data
df = pd.read_csv('intro_bees.csv')
print(df.head())

df = df.groupby(['State', 'ANSI', 'Affected by',
              'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace = True)

# ----------------- App Layout
app.layout = html.Div([

    html.H1('Challenge A', style= {'text-align': 'center'}),

    dcc.Dropdown(id = 'slct-year', 
    options = [
        {'label': '2015', 'value': 2015},
        {'label': '2016', 'value': 2016},
        {'label': '2017', 'value': 2017},
    ],
    multi = False,
    value = 2015,
    style = {'width' : '40%'},
    ),

    html.Div(id = 'output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_bar', figure = {}),

])


# ------------- connect plotly graphs with Dash Components using callback

@app.callback([
    Output(component_id='output_container', component_property='children'),
    Output(component_id='my_bee_bar', component_property='figure'),
    Input(component_id='slct-year', component_property='value'),
])


def update_graph(option_slctd):

    container = 'The year chosen by user is: {}'.format(option_slctd)

    # make a copy of the df
    dff = df.copy()
    dff = dff[dff['Year'] == option_slctd]
    dff = dff[dff['Affected by'] == 'Varroa_mites']


    # plotly express
    fig = px.bar(
        data_frame = dff,
        x = 'State',
        y = 'Pct of Colonies Impacted',
        hover_data=['State', 'ANSI'],
        template='plotly_dark'
    )

    return container, fig


## --------------------- run the app
if __name__ == "__main__":
    app.run_server(debug = True)