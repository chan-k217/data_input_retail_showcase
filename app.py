# %%
# # DO NOT MODIFY
# from jupyter_dash import JupyterDash
# from datasets import load_data

# JupyterDash.infer_jupyter_proxy_config()
# app = JupyterDash(__name__, external_stylesheets=['https://ikigai-css-stylesheets.s3.us-east-2.amazonaws.com/dash_dark-theme.css?v=1.0.6'])
# data = load_data()

# %%
from jupyter_dash import JupyterDash
app = JupyterDash(__name__, external_stylesheets=['https://ikigai-css-stylesheets.s3.us-east-2.amazonaws.com/dash_dark-theme.css?v=1.0.6'])

# %%
import requests
import pandas as pd
def get_dataset(dataset_id):
    url = f"https://api.ikigailabs.io/pypr/get-dataset-download-url?dataset_id={dataset_id}"

    payload = {}
    headers = {
    'User': 'demo@ikigailabs.io',
    'Api-key': '2S2bcHagJLgme4jI5FWdpN028PE',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    df = pd.read_csv(response.json()['url'])
    return df


# %%
input_left_merchant = get_dataset('2a5qrZvT7876y7WmqF7xKHWvk8M')
input_right_product = get_dataset('2a5qtbrxnQ11GY5RE0Wg22BP60E')
data_2020wdates = get_dataset('2a5qoqn2fxmAnKifP1XfdbCiE1z')

# %%
import os
import base64
import datetime
import io
import random
import math

import dash
#import dash_table
from dash import dash_table
import dash_daq as daq
from dash import dcc
from dash import html
import dash_table.FormatTemplate as FormatTemplate

import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

from dash.dependencies import Input, Output, State


# %%


# Read csv files (tab 1)
# exceptions_left = data['Input_Left (Merchant)']
# exceptions_right = data['Input_Right (Product)'].sample(frac=1)
# original = data['2020wdates'][['product_id', 'product_picture']].drop_duplicates()

exceptions_left = input_left_merchant
exceptions_right = input_right_product
original = data_2020wdates[['product_id', 'product_picture']].drop_duplicates()

# %%


exceptions_right.insert(0, 'product_picture_markdown_right', exceptions_right['product_picture_right'].apply(lambda x: "![product_picture_right](" + str(x) + ")"))
print(exceptions_left)

exceptions_left.insert(0, 'product_picture_markdown_left',
                       exceptions_left.merge(original, left_on='product_id_left',
                                             right_on='product_id')['product_picture'].apply(lambda x: "![product_picture_left](" + str(x) + ")"))
# Drop right product IDs
#exceptions_right = exceptions_right.drop(columns='product_id_right')
exceptions_left = exceptions_left[['product_picture_markdown_left', 'title_orig_left', 'merchant_title_left', 'merchant_rating_left']]
exceptions_right = exceptions_right[['product_picture_markdown_right', 'title_right', 'SKU', 'Store', 'product_color_right', 'product_variation_size_id_right', 'price_right', 'rating_right']]

exceptions_left = exceptions_left.rename(columns={'product_picture_markdown_left': 'Product Image (Left)',
                                'title_orig_left': 'Title Original (Left)',
                                'merchant_title_left': 'Merchant Title (Left)',
                                'merchant_rating_left': 'Merchant Rating (Left)'})

exceptions_right = exceptions_right.rename(columns={'product_picture_markdown_right':'Product Image (Right)',
                                                    'title_right':'Title (Right)',
                                                    'product_color_right':'Product Color (Right)',
                                                    'product_variation_size_id_right':'Product Size (Right)',
                                                    'price_right': 'Price (Right)',
                                                    'rating_right':'Rating (Right)'})
"""
Helper Functions
"""

def exceptions_div(data):
    table = []
    table_header = []
    table_body = []
    columns = list(data)
    table_header.append(html.Div("", className="table-header-checkbox"))
    for key, valuesArray in data.iteritems():
        table_header.append(html.Div(key, className="table-header-col"))
        if key == "Reason" or key == "Order Number":
            table_header.append(html.Div("", className="table-header-break"))
    for i in data.itertuples(index = False):
        row_columns_temp = []
        columnCounter = 0
        row_columns_temp.append(html.Div(
            dcc.Checklist(
                inputClassName="checkbox-input",
                labelClassName="checkbox-label",
                options=[
                    {'label': '', 'value': 'checked'}
                ],
                value=['']
            )
        , className="table-column has-checkbox"))
        for j in i:
            if columns[columnCounter] == "Order Number":
                row_columns_temp.append(html.Div(dcc.Dropdown(
                    options=[
                        {"label": i, "value": i} for i in forecasts["SKU"].astype(str).unique()
                    ],
                    value=j
                ), className="table-column has-dropdown")),
            else:
                row_columns_temp.append(html.Div(j, className="table-column"))
            if columns[columnCounter] == "Reason" or columns[columnCounter] == "Order Number":
                row_columns_temp.append(html.Div("", className="table-column-break"))
            columnCounter += 1
        table_body.append(html.Div(row_columns_temp, className="table-row"))
    table.append(html.Div([
        html.Div(table_header, className="table-head"),
        html.Div(table_body, className="table-body")
    ], className="custom-div-table-inner"))
    return html.Div(table, className="custom-div-table")


def matched_div(data):
    table = []
    table_header = []
    table_body = []
    columns = list(data)
    table_header.append(html.Div("", className="table-header-checkbox"))
    for key, valuesArray in data.iteritems():
        table_header.append(html.Div(key, className="table-header-col"))
        if key == "Order Number":
            table_header.append(html.Div("", className="table-header-break"))
    for i in data.itertuples(index = False):
        row_columns_temp = []
        columnCounter = 0
        row_columns_temp.append(html.Div("", className="table-column has-x"))
        for j in i:
            row_columns_temp.append(html.Div(j, className="table-column"))
            if columns[columnCounter] == "Order Number":
                row_columns_temp.append(html.Div("", className="table-column-break"))
            columnCounter += 1
        table_body.append(html.Div(row_columns_temp, className="table-row"))
    table.append(html.Div([
        html.Div(table_header, className="table-head"),
        html.Div(table_body, className="table-body")
    ], className="custom-div-table-inner"))
    return html.Div(table, className="custom-div-table")

def inventory_div(data):
    table = []
    table_header = []
    table_body = []
    columns = list(data)
    for key, valuesArray in data.iteritems():
        table_header.append(html.Div(key, className="table-header-col"))
    for i in data.itertuples(index = False):
        row_columns_temp = []
        columnCounter = 0
        for j in i:
            if columns[columnCounter] == "Remaining Quantity" and j < 500:
                row_columns_temp.append(html.Div(
                    html.Div(j, className="alert-error")
                    , className="table-column number"))
            elif columns[columnCounter] == "Remaining Quantity":
                row_columns_temp.append(html.Div(j, className="table-column number"))
            else:
                row_columns_temp.append(html.Div(j, className="table-column"))
            columnCounter += 1
        table_body.append(html.Div(row_columns_temp, className="table-row"))
    table.append(html.Div([
        html.Div(table_header, className="table-head"),
        html.Div(table_body, className="table-body")
    ], className="custom-div-table-inner"))
    return html.Div(table, className="custom-div-table")

def reorder_form_div(data):
    table = []
    table_header = []
    table_body = []
    columns = list(data)
    table_header.append(html.Div("", className="table-header-checkbox"))
    for key, valuesArray in data.iteritems():
        table_header.append(html.Div(key, className="table-header-col"))
    for i in data.itertuples(index = False):
        row_columns_temp = []
        columnCounter = 0
        row_columns_temp.append(html.Div("", className="table-column has-x"))
        for j in i:
            row_columns_temp.append(html.Div(j, className="table-column"))
            columnCounter += 1
        table_body.append(html.Div(row_columns_temp, className="table-row"))
    table.append(html.Div([
        html.Div(table_header, className="table-head"),
        html.Div(table_body, className="table-body")
    ], className="custom-div-table-inner"))
    return html.Div(table, className="custom-div-table")

def get_line_breaks(n):
    breaks = []
    for i in range(n):
        breaks.append(html.Br())
    return html.Div(breaks)


def get_dropdown_columns(columns):
    dropdown_columns = ["Order Number", "Lot Code", "Purchase Order"]
    currency_columns = ["Price", "Cost"]
    columns_list = []
    for i in columns:
        if 'Image' in i:
            columns_list.append({"name": i, "id": i, "presentation": "markdown"})
        elif i in dropdown_columns:
            columns_list.append({"name": i, "id": i, "presentation": "dropdown"})
        elif i == "Invoice Due Date":
            columns_list.append({"name": i, "id": i, "type": "datetime", 'on_change': {'action': 'none'}})
        elif i in currency_columns:
            columns_list.append({"name": i, "id": i, 'type': 'numeric', 'format': FormatTemplate.money(0)})
        else:
            columns_list.append({"name": i, "id": i})
    return columns_list


def get_non_dropdown_columns(columns):
    currency_columns = ["Price", "Cost"]
    columns_list = []
    for i in columns:
        if 'Image' in i:
            columns_list.append({"name": i, "id": i, "presentation": "markdown"})
        elif i == "Invoice Due Date":
            columns_list.append({"name": i, "id": i, "type": "datetime", 'on_change': {'action': 'none'}})
        elif i in currency_columns:
            columns_list.append({"name": i, "id": i, 'type': 'numeric', 'format': FormatTemplate.money(0)})
        else:
            columns_list.append({"name": i, "id": i})
    return columns_list


"""
Data Table and Graph Functions
"""


def generate_table(dataframe, name):
    return dash_table.DataTable(
        id=name,
        columns=get_non_dropdown_columns(dataframe.columns),
        data=dataframe.to_dict('records'),
        fixed_rows={'headers': True, 'data': 0},
        style_cell={
            'textAlign': 'left'
        },
    )


def generate_editable_table(dataframe, name):
    return dash_table.DataTable(
        id=name,
        columns=get_non_dropdown_columns(dataframe.columns),
        data=dataframe.to_dict('records'),
        editable=True,
        row_deletable=True,
        fixed_rows={'headers': True, 'data': 0},
        style_cell={
            'textAlign': 'left',
            'minWidth': '60px', 'width': '180px', 'maxWidth': '180px',
        },
        style_data_conditional=[
            {
                'if': {
                    'column_id': 'Remaining Quantity',
                    'filter_query': '{Remaining Quantity} < 500',
                },
                'color': '#d82525',
                'fontSize': '14px',
                'backgroundColor': '#ffeaea',
                'border': '1px solid hsla(0,0%,85.9%,.4)',
                'borderRadius': '5px',
                'padding': '1px 6px',
                'fontWeight': '500',
            },
            {
                'if': {
                    'column_id': 'Purchase Order',
                },
            },
            {
                'if': {
                    'column_id': 'Lot Code',
                },
            },
            {
                'if': {
                    'column_id': 'Manufacture Date',
                },
            },
            {
                'if': {
                    'column_id': 'Shipment Date',
                },
            },
        ]
    )


def generate_exportable_table(dataframe, name):
    return dash_table.DataTable(
        id=name,
        columns=get_non_dropdown_columns(dataframe.columns),
        data=dataframe.to_dict('records'),
        fixed_rows={'headers': True, 'data': 0},
        export_format='csv',
        style_cell={
            'textAlign': 'left'
        },
    )


def generate_prioritized_table(dataframe, name):
    return dash_table.DataTable(
        id=name,
        columns=[{"name": i, "id": i} for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        fixed_rows={'headers': True, 'data': 0},
        sort_action="native",
        style_cell={
            'textAlign': 'left',
            'minWidth': '60px', 'width': '180px', 'maxWidth': '180px',
        },
        style_data_conditional=[
            {
                'if': {
                    'column_id': 'Remaining Quantity',
                    'filter_query': '{Remaining Quantity} < 500',
                },
                'color': '#d82525',
                'fontSize': '14px',
                'backgroundColor': '#ffeaea',
                'border': '1px solid hsla(0,0%,85.9%,.4)',
                'borderRadius': '5px',
                'padding': '1px 6px',
                'fontWeight': '500',
            }
        ]
    )


def generate_exceptions_table(dataframe, name):
    return dash_table.DataTable(
        id=name,
        columns=get_dropdown_columns(dataframe.columns),
        data=dataframe.to_dict('records'),
        editable=True,
        row_selectable="multi",
        
        #Table Height 
        fixed_rows={'headers': True, 'data': 0},
        style_table={'height': 1000},  # default is 500
        virtualization=True,
        
        # Wrap Text
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto'},
       
        style_cell={
            'textAlign': 'left',
            'minWidth': '60px', 'width': '180px', 'maxWidth': '180px'
        }
    )


def generate_graph(dataframe, name, x, y):
    graph = dcc.Graph(
        id=name,
        figure={
            'data': [
                {'x': dataframe[x].values.tolist(), 'y': dataframe[y].values.tolist(),
                 'type': 'line', 'name': name},
            ],
            'layout': {
                'plot_bgcolor': "#23272c",
                'paper_bgcolor': "#23272c",
                'font': {'color': "#a3a7b0"}
            }
        }
    )
    return graph


def generate_bar_graph(dataframe, name, x, y):
    graph = dcc.Graph(
        id=name,
        figure={
            'data': [
                {'x': dataframe[x].values.tolist(), 'y': dataframe[y].values.tolist(),
                 'type': 'bar', 'name': name},
            ],
            'layout': {
                'plot_bgcolor': "#23272c",
                'paper_bgcolor': "#23272c",
                'font': {'color': "#a3a7b0"}
            }
        }
    )
    return graph

def generate_horizontal_bar_graph(dataframe, name, x, y):
    graph = dcc.Graph(
        id=name,
        figure={
            'data': [
                {'x': dataframe[x].values.tolist(), 'y': dataframe[y].values.tolist(),
                 'type': 'bar', 'name': name, 'orientation': 'h'},
            ],
            'layout': {
                'plot_bgcolor': "#23272c",
                'paper_bgcolor': "#23272c",
                'font': {'color': "#a3a7b0"},
                'margin': {'l': "300"}
            }
        }
    )
    return graph


def generate_sunburst_graph(name, labels, parents, values):
    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
    ))
    fig.layout = dict(plot_bgcolor="#23272c", paper_bgcolor="#23272c", font=dict(color="#a3a7b0"), margin=dict(t=0, l=0, r=0, b=0))
    graph = dcc.Graph(
        id=name,
        figure=fig
    )
    return graph


def get_graph(input_data, velocity=0, days_out=90):
    expenses_knob = 0
    inventory_knob = 0
    
    date = input_data[input_data['Model'] == 'Real']['Date'].max()
    stop_date = pd.to_datetime(date) + datetime.timedelta(days=days_out)
    input_data = input_data[pd.to_datetime(input_data['Date']) <= stop_date]
    grouped = input_data.groupby(['Date', 'Model']).sum().reset_index().drop(columns=['Savings', 'Store', 'SKU'])
    
    reals = grouped[grouped['Model'] == 'Real']
    arima = grouped[grouped['Model'] == 'ARIMA']
    deepcast = grouped[grouped['Model'] == 'DeepCast']
    holt_winters = grouped[grouped['Model'] == 'Holt-Winters']
    prophet = grouped[grouped['Model'] == 'PROPHET']
    
    if velocity != 0:
        arima['Weekly_Sales'] = arima['Weekly_Sales'] * ((velocity + 201) / 200)
        deepcast['Weekly_Sales'] = deepcast['Weekly_Sales'] * ((velocity + 201) / 200)
        holt_winters['Weekly_Sales'] = holt_winters['Weekly_Sales'] * ((velocity + 201) / 200)
        prophet['Weekly_Sales'] = prophet['Weekly_Sales'] * ((velocity + 201) / 200)


    cash_flow_graph = dcc.Graph(
        id="cash-flow",
        figure={
            'data': [
                {'x': arima['Date'].values.tolist(),
                 'y': arima['Weekly_Sales'].values.tolist(),
                 'type': 'line', 'name': 'ARIMA', 'line': {'shape': 'spline', 'width': 3}
                 },
                {'x': deepcast['Date'].values.tolist(),
                 'y': deepcast['Weekly_Sales'].values.tolist(),
                 'type': 'line', 'name': 'DeepCast', 'line': {'shape': 'spline', 'width': 3}
                 },
                {'x': holt_winters['Date'].values.tolist(),
                 'y': holt_winters['Weekly_Sales'].values.tolist(),
                 'type': 'line', 'name': 'Holt-Winters', 'line': {'shape': 'spline', 'width': 3}
                 },
                {'x': prophet['Date'].values.tolist(),
                 'y': prophet['Weekly_Sales'].values.tolist(),
                 'type': 'line', 'name': 'Prophet', 'line': {'shape': 'spline', 'width': 3}
                 },
                {'x': reals['Date'].values.tolist(),
                 'y': reals['Weekly_Sales'].values.tolist(),
                 'type': 'line', 'name': 'Historical Sales',
                 'line': {'shape': 'spline', 'width': 3, 'color': '#836fbf'}
                 },
            ],
            'layout': go.Layout(
                shapes=[
                    {
                        'type': 'line',
                        'x0': date,
                        'y0': 0,
                        'x1': date,
                        'y1': reals['Weekly_Sales'].max(),
                        'line': {'color': '#a3a7b0', 'width': 2}
                    }
                ],
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font=dict(
                    color="#a3a7b0"
                ),
                #height=1275,
                legend=dict(font=dict(size=30))
            )
        },
        style={"height": 1275}
    )
    

    return cash_flow_graph


"""
Default Graphs and Tables
"""
# Tab 1
deep_input_left_table = generate_exceptions_table(exceptions_left, "tab1_table0")
deep_input_right_table = generate_exceptions_table(exceptions_right, "tab1_table1")

"""
APP LAYOUT
"""
tab1_layout = html.Div([
#Apply DeepMatch to Data Button
        html.Div([
            html.Div([
                    html.A(html.Button('🔀 Apply DeepMatch to Data', id='applydeepmatch', n_clicks=0, className="iki-button iki-primary"), href="https://dashboard.ikigailabs.io/erZj"),
                ], className="iki-button-holder"),
            ], className="iki-row center-content"),
    
        html.Div([
            html.Div([
                html.Div([
                    html.H1('Left Input Table'),
                    get_line_breaks(1),
                    
                    # Upload Left Data Box
                    html.Div([
                    dcc.Upload(
                        id="upload-data-left",
                        children=html.Div([
                            "Left Input Table: Drag and drop or ",
                            html.A("select a file")
                        ]),
                        style={
                            "width": "100%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "margin": "10px"
                        },
                        multiple=False,
                    ),
                    html.Div(id="output-data-left")
                    ]),
                    ##

                    html.H3('Merchants'),
                    html.Div([deep_input_left_table], className="iki-table-grid"),
                    get_line_breaks(2),
                ], className="iki-col-box has-table"),
            ], className="iki-column iki-col1-2"),
            
            html.Div([
                html.Div([
                    html.H1('Right Input Table'),
                    get_line_breaks(1),
                    
                    # Upload Right Data Box
                    html.Div([
                    dcc.Upload(
                        id="upload-data-right",
                        children=html.Div([
                            "Right Input Table: Drag and drop or ",
                            html.A("select a file")
                        ]),
                        style={
                            "width": "100%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "margin": "10px"
                        },
                        multiple=False,
                    ),
                    html.Div(id="output-data-right")
                    ]),
                    ##
                    
                    html.H3('Products & Ratings'),
                    html.Div([deep_input_right_table], className="iki-table-grid"),
                    get_line_breaks(2),
                ], className="iki-col-box has-table"),
            ], className="iki-column iki-col1-2"),
        ], className="iki-row")
    ], className="iki-grid",
)


app.layout = html.Div([
    html.Div([
        html.Img(width= 250, src="https://assets.website-files.com/62bda440dae2cfc77f6cf93b/62bda440dae2cf6f406cf9ed_logo__footer.svg", style={"margin-top": "20px"}),
        html.H1('Data Input: Connect to any data source in no time', style={"margin-top": "20px"}),
        html.H3('Powered by Ikigai'),
        html.H4('We support more than 150 data integrations out of the box - no code necessary. We can add any connector you need in minutes.'),        
        tab1_layout
    ]),
    html.Div(id="data-storage", style={'display': 'none'})
])

# %%
# DO NOT MODIFY
# app.run_server(mode='inline')

# %%
# DO NOT MODIFY
app.run_server(mode='external')

# %%


# %%


# %%
