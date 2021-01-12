# https://www.youtube.com/watch?v=USTqY4gH_VM

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import dash_table

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# ---------------- import and work data
df = pd.read_csv('data/internet_cleaned.csv')
df = df[df['year'] == 2019]

### create an id col name gives us more interactive capabilities
df['id'] = df['iso_alpha3']
df.set_index('id', inplace = True, drop = False)
# print(df.columns)


# ------------ app layout
# sorting operators (https://dash.plotly.com/datatable/interactivity)
app = dash.Dash(__name__, prevent_initial_callbacks=True)

app.layout = html.Div(
    [
        dash_table.DataTable(
            id = 'datatable-interactivity',


            ### we are doing this so that tables of the id, which are not that important can be hidden
            columns = [
                {
                    'name': i,
                    'id': i,
                    'deletable': True,
                    'selectable': True,
                    'hideable': True,
                } 
                if i == 'iso_alpha3' or i == 'year' or i == 'id'

                ### while those that are more important, will not be hideable
                else {
                    'name': i,
                    'id': i,
                    'deletable': True,
                    'selectable': True,
                }
                for i in df.columns
            ],

            data = df.to_dict('records'), # the contents of the datatable
            editable = True, # can edit in the datatable!!
            filter_action = 'native', # or none
            sort_action = 'native', # or none
            sort_mode = 'multi', # or single
            column_selectable = 'multi', # or single
            row_selectable = 'multi', # or single
            row_deletable = True,
            selected_columns = [],
            selected_rows = [],
            page_action = 'native',
            page_current = 0,
            page_size = 6, # number of rows visible per page
            style_cell = { 
                # ensure adequate header width when text is shorter than cell's text
                'minWidth': 95,
                'maxWidth': 95,
                'width': 95,

            },
            style_cell_conditional = [
                # in spreadsheet culture, 
                # numbers are aligned right
                # text is aligned left!
                # by default, everything is aligned right
                {
                    'if': {'column_id': c},
                    'textAlign': 'left'
                } 
                for c in ['country', 'iso_alpha3']
            ],
            style_data ={
                # basically text wrapping!
                'whiteSpace' : 'normal',
                'height' : 'auto'
            }
        ),

        html.Br(),
        html.Br(),

        html.Div(id='bar-container'),
        html.Div(id='choromap-container'),
    ]
)


### connect graph to app ------------

## BarChart
@app.callback(
    Output('bar-container', component_property = 'children'),
    [
        Input('datatable-interactivity', 'derived_virtual_data'),
        Input('datatable-interactivity', 'derived_virtual_selected_rows'),
        Input('datatable-interactivity', 'derived_virtual_selected_row_ids'),
        Input('datatable-interactivity', 'selected_rows'),
        Input('datatable-interactivity', 'derived_virtual_indices'),
        Input('datatable-interactivity', 'derived_virtual_row_ids'),
        Input('datatable-interactivity', 'active_cell'),
        Input('datatable-interactivity', 'selected_cells'),
    ]
)
def update_bar(all_rows_data, slctd_row_indices, slct_rows_names, slctd_rows, order_of_rows_indices, order_of_rows_names, actv_cell, slcted_cell):
    #print('**************************************')
    #print('Data across all pages pre or post filtering: {}'.format(all_rows_data))

    #print('-------------------------------------')
    #print('Indices of selected rows of part of table after filtering: {}'.format(slctd_row_indices))
    #print('Names of selected rows of part of table after filtering: {}'.format(slct_rows_names))
    #print('Indices of selected rows regardless of filtering: {}'.format(slctd_rows))

    #print('-------------------------------------')
    #print('Indices of all rows pre or post filtering: {}'.format(order_of_rows_indices))
    #print('Names of all rows pre or post filtering: {}'.format(order_of_rows_names))


    #print('Complete data of active cell: {}'.format(actv_cell))
    #print('Complete data of all selected cells cell: {}'.format(slcted_cell))

    print('**************************************')
    print('derived virtual data: {}'.format(all_rows_data))

    print('-------------------------------------')
    print('derived virtual selected row: {}'.format(slctd_row_indices))
    print('derived virtual selected row ids: {}'.format(slct_rows_names))
    print('selected rows: {}'.format(slctd_rows))

    print('-------------------------------------')
    print('derived virtual indices: {}'.format(order_of_rows_indices))
    print('derived virtual row ids: {}'.format(order_of_rows_names))


    print('-------------------------------------')
    print('active cell: {}'.format(actv_cell))
    print('selected cell: {}'.format(slcted_cell))
    dff = pd.DataFrame(all_rows_data)

    colors = ['pink' if i in slctd_row_indices else 'blue' for i in range(len(dff))]

    fig = px.bar(
        dff,
        x = 'country',
        y = 'did online course',
        labels = {
            'did online course': '% of Pop took online course',
        }
    )
    fig.update_layout(showlegend = False)
    fig.update_traces(marker_color = colors, hovertemplate = '<b>%{y}%</b><extra></extra>')

    if 'country' in dff and 'did online course' in dff:
        return [
            dcc.Graph(
                id = 'bar-chart',
                figure = fig
            )
        ]


@app.callback(
    Output('choromap-container', 'children'),
    [
        Input('datatable-interactivity', 'derived_virtual_data'),
        Input('datatable-interactivity', 'derived_virtual_selected_rows'),
    ]
)
def update_map(all_rows_data, slctd_row_indices):
    dff = pd.DataFrame(all_rows_data)

    # highlight selected countries on map
    borders = [6 if i in slctd_row_indices else 1 for i in range(len(dff))]

    if 'iso_alpha3' in dff and 'internet daily' in dff and 'country' in dff:
        return [
            dcc.Graph(
                id = 'choropleth',
                style = {
                    'height': 700
                },
                figure = px.choropleth(
                    data_frame=dff,
                    locations = 'iso_alpha3',
                    scope='europe',
                    color='internet daily',
                    title='% of Pop that uses internet daily',
                    template = 'plotly_dark',
                    hover_data=['country', 'internet daily'],
                ).update_layout(showlegend = False, title = dict(
                    font = dict(size = 28), x = 0.5, xanchor = 'center'
                )).update_traces(
                    marker_line_width = borders,
                    # hoverteI
                )
            )
        ]




# run the app ----------------------
if __name__ == "__main__":
    app.run_server(debug=True)