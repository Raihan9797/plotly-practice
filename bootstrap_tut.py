import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import pandas_datareader.data as web
import datetime


# start = datetime.datetime(2020, 1, 1)
# end = datetime.datetime(2020, 12, 3)
# df = web.DataReader(['AMZN', 'GOOGL', 'FB', 'PFE', 'BNTX', 'MRNA'], 'stooq', start=start, end = end)
# df = df.stack().reset_index()
# df.to_csv('mystocks.csv', index = False)

df = pd.read_csv('data/mystocks.csv')
# print(df[:15])


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale = 1.0'}]
                            )

# Layout Section: Bootstrap
# -----------------------------------------------------

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Stock Market Dashboard',
        className = 'text-center text-primary mb-4'), 
        width = 12)

    ]),
    dbc.Row([
        dbc.Col(
        [
            dcc.Dropdown(id = 'my-dpdn', multi = False, value = 'AMZN',
            options = [{'label': x, 'value': x} for x in sorted(df['Symbols'].unique())]),

            # fig is so we can see an empty graph!
            dcc.Graph(id='line-fig', figure={})
        ], 
        # width = {'size': 5, 'offset': 0},
        xs=12, sm=12, lg=5, xl=5,
        ),
        dbc.Col([
            dcc.Dropdown(id = 'my-dpdn2', multi = True, value = ['PFE', 'BNTX'], 
            options = [
                {'label': x, 'value': x}
                for x in sorted(df['Symbols'].unique())
            ]),

            dcc.Graph(id = 'line-fig2', figure = {})
            # 'order': 1
        ], 
        # width = {'size': 5},
        xs=12, sm=12, lg=5, xl=5,
        
        )
    ],
    # justify: start end center between around
    no_gutters=False, justify='around'),



    dbc.Row([
        dbc.Col([
            html.P('Select company Stock', 
            style = {'textDecoration': 'underline'}),

            dcc.Checklist(id = 'my-checklist', value= ['FB', 'GOOGL', 'MRNA'], 
            options = [
                {'label': x, 'value': x} for x in sorted(df['Symbols'].unique())
            ], 
            labelClassName = 'mr-4 text-success text-monospace'), # spacing, color and font changes

            dcc.Graph(id = 'my-hist', figure = {})
        ], 
        # width = {'size': 5, 'offset': 0},
        xs=12, sm=12, lg=5, xl=5,
        ),


        dbc.Col([
            dbc.Card(
                [
                    dbc.CardImg(src='/assets/dash.png', top=True, style={'width': 50, 'content-align': 'center'}, className = 'align-self-center'), # styling the card image
                    dbc.CardBody(
                        [
                            html.H1('Card title', className = 'card-title'),
                            html.P('this is a html paragrapg inside a dbc cardBody which is inside a dbc.Card', className = 'card-text'),

                        ]
                    ),
                ]
                ,style = dict(width = '24rem')
                # , style = {'width': 40} # styles the entire card
            )

        ],
        # width = {'size': 5, 'offset': 0},
        xs=12, sm=12, lg=5, xl=5,

        )
    ],
    ),

    # new_row, # ----------------1 stock go line fig
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Dropdown(
                        id = 'linefiggo-dpdn',
                        value = 'GOOGL',
                        options = [
                            {'label': x, 'value': x} for x in sorted(df['Symbols'].unique())
                        ],
                        multi = False,

                    ),
                    dcc.Graph(
                        id='linefiggo',
                        figure = {}
                    )
                ]
            ),

            dbc.Col(
                [
                    dcc.Checklist(
                        id = 'bargo-checklist',
                        value = ['GOOGL', 'AMZN'],
                        options = [
                            {'label': x, 'value': x} for x in sorted(df['Symbols'].unique())
                        ]
                    ),

                    dcc.Graph(
                        id = 'bargo',
                        figure = {},
                    )
                ]
            )
        ]
    )

], fluid= True)






## callbacks

# Line Chart = Single
@app.callback(
    Output(component_id='line-fig', component_property='figure'),
    Input(component_id='my-dpdn', component_property='value')
)
def update_graph(stock_slctd):
    dff = df.copy()
    dff = dff[dff['Symbols'] == stock_slctd]

    figln = px.line(
        data_frame= dff,
        x = 'Date',
        y = 'Close'
    )
    return figln

# Line Chart Multi Select
@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value'),
)
def update_graph(stock_slctd):
    dff = df.copy()
    dff = dff[dff['Symbols'].isin(stock_slctd)]

    figln2 = px.line(
        dff,
        x= 'Date',
        y = 'Open',
        color='Symbols'
    )
    return figln2

# Bar Chart
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value'),
)
def update_graph(stock_slctd):
    dff = df.copy()
    dff = dff[dff['Symbols'].isin(stock_slctd)]
    dff = dff.groupby(['Symbols']).sum()
    # print(dff)

    bar = px.bar(
        dff,
        x = dff.index,
        y = 'Close',
        labels= {'Close': 'Sum of Closes'},
    )
    bar.update_layout(
        title= 'Sum Of Total Closing Stock Prices',
        title_x = 0.5,
    )

    return bar

### ----------------single line fig using graph_objects -------------------------
import plotly.graph_objects as go
@app.callback(
    Output('linefiggo', 'figure'),
    Input('linefiggo-dpdn', 'value')
)
def update_graph(stock_slctd):
    # dff = df.copy()
    # dff = dff[dff['Symbols'] == stock_slctd]
    # figln = px.line(
    #     data_frame= dff,
    #     x = 'Date',
    #     y = 'Close'
    # )

    # graph objects example
    dfg = df.copy()
    dfg = dfg[dfg['Symbols']== stock_slctd]

    linefiggo = go.Figure()
    linefiggo.add_trace(
        go.Scatter(
            x = dfg['Date'],
            y = dfg['Close']
        )
    )
    return linefiggo

### ----------------bar using graph_objects ------------
@app.callback(
    [
        Output('bargo', 'figure'),
        Input('bargo-checklist', 'value'),
    ]
)
def update_layout(options_slctd):
    dff = df.copy()
    dff = dff[dff['Symbols'].isin(options_slctd)]
    dff = dff[dff['Date'] == '2020-12-03']
    print(dff['Symbols'])
    print(dff['Close'])


    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x = ['a', 'b', 'c'],
            y = dff[10, 20, 30],
        )
    )

    return fig

    

if __name__ == "__main__":
    app.run_server(debug = True)