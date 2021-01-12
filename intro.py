import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
# import plotly.graph_objects as go

#----------------- start the app
app = dash.Dash(__name__)



#----------------- get and clean the data
df = pd.read_csv("data/intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace = True)
print(df.head())

#----------------- App Layout
app.layout = html.Div([

    html.H1('Web Application Dashboards with Dash', style = {'text-align': 'center'}),

    dcc.Dropdown(id = 'slct-year',
        options = [
            {'label': '2015', 'value': 2015},
            {'label': '2016', 'value': 2016},
            {'label': '2017', 'value': 2017},
        ],
        multi = False,
        value = 2015,
        style = {'width': '40%'}
    ),


    html.Div(id = 'output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure = {})

])

#----------------- Connect Plotly grapsh with Dash Components using Callback

# we use component_id and component_property to connect the 2

# we are outputting to my+bee+app and output_container
# its gonna output to the children and figure property
# usually we dont need to do that, but this was made for example purposes
@app.callback([
    Output(component_id='output_container', component_property='children'),
    Output(component_id='my_bee_map', component_property='figure'),
    Input(component_id='slct-year', component_property='value')
]
)

# each argument relates to one input
# since we are only using slct-yr, we only have one argument
# value--> option_slctd


# what you return will go to the output
# since we have 2 outputs, we need to return 2 elements!!
def update_graph(option_slctd):
    # print(option_slctd)
    # print(type(option_slctd))

    container = 'The year chosen by user was:: {}'.format(option_slctd)

    # make a copy of the df
    dff = df.copy()
    dff = dff[dff['Year'] == option_slctd]
    dff = dff[dff['Affected by'] == 'Varroa_mites']
    print(dff.head())

    # plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope='usa',
        color='Pct of Colonies Impacted',
        hover_data=['State', 'ANSI'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        template='plotly_dark'
    )

    # Plotly graph objects (GO)
    import plotly.graph_objects as go
    fig = go.Figure(
        data = [
            go.Choropleth(
                locationmode='USA-states',
                locations= dff['state_code'],
                z = dff['Pct of Colonies Impacted'].astype(float),
                colorscale = 'Reds',
            )
        ]
    )

    fig.update_layout(
        title_text = 'graph objects example',
        title_xanchor = 'center',
        title_font = dict(size=24),
        title_x = 0.5,
        geo = dict(scope = 'usa')
    )


    return container, fig,






#----------------- run the app

if __name__ == '__main__':
    app.run_server(debug = True)