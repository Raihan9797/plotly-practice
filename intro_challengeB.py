# challenge B: Line chart
# x = year, y - % bee colonies, color - state
# dropdown: list of things affecting bees

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd


## -------------- create app
app = dash.Dash(__name__)


## -------------- get and clean data
df = pd.read_csv('data/intro_bees.csv')

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace = True)


## -------------- app layout
app.layout = html.Div([

    html.H1('Challenge B', style = {'text-align': 'center'}),

    dcc.Dropdown(id = 'slct-effect',
    options = [
        {'label': 'Disease', 'value' : 'Disease'},
        {'label': 'Other', 'value' : 'Other'},
        {'label': 'Pesticides', 'value' : 'Pesticides'},
        {'label': 'Pests excluding Varroa', 'value' : 'Pests_excl_Varroa'},
        {'label': 'Unknown', 'value' : 'Unknown'},
        {'label': 'Varroa mites', 'value' : 'Varroa_mites'},
    ],
    value = 'Disease',
    multi = False,
    ),

    html.Div(id= 'output_container', children = []),
    html.Br(),

    dcc.Graph(id = 'my_bee_line', figure = {}),
])

## -------------- callbacks

@app.callback([
    Output(component_id='output_container', component_property='children'),
    Output(component_id='my_bee_line', component_property='figure'),
    Input(component_id='slct-effect', component_property='value'),
])

def update_graph(option_slctd):
    print(option_slctd)

    container = 'The effect chosen by user is {}'.format(option_slctd)

    dff = df.copy()
    dff = dff[dff['Affected by'] == option_slctd]
    dff = dff[
        (dff['State'] == 'Idaho') |
        (dff['State'] == 'New York') |
        (dff['State'] == 'Texas')
    ]


    figure = px.line(
        data_frame=dff,
        x = 'Year',
        y = 'Pct of Colonies Impacted',
        color='State',
        hover_data=['ANSI', 'Pct of Colonies Impacted']
    )

    return container, figure



## -------------- run the app
if __name__ == "__main__":
    app.run_server(debug=True)