# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output
from dash import html

sales_data = pd.read_excel('Online Retail.xlsx', sheet_name=None)
print('Sheets in the excel are {}'.format(sales_data.keys()))
ecom_sales = sales_data['Online Retail']
ecom_sales['OrderValue'] = ecom_sales['UnitPrice'] * ecom_sales['Quantity']
ecom_sales['Year-Month'] = ecom_sales['InvoiceDate'].map(lambda x: "{}-{}".format(x.year, x.month))

fig1 = px.bar(x=ecom_sales.groupby(['Year-Month'])['OrderValue'].sum().index,
              y=ecom_sales.groupby(['Year-Month'])['OrderValue'].sum().tolist(), title='Total Sales')
fig1.update_xaxes(title_text='Month-Year of the sales', tickangle=90,
                  tickvals=ecom_sales.groupby(['Year-Month'])['Year-Month'].sum().index)
fig1.update_yaxes(title_text='Order value in year-month')

countries = ecom_sales.Country.unique()
year_month = ecom_sales['Year-Month'].unique()
order_values = []
for c in countries:
    c_df = ecom_sales[ecom_sales["Country"]==c]
    sales = []
    for date in year_month:
        sales.append(c_df[c_df['Year-Month']==date]['OrderValue'].mean())
    order_values.append([0.0 if np.isnan(x) else x for x in sales])

# fig = px.line(x=ecom_sales.groupby(['Year-Month'])['OrderValue'].sum().index,
#               y=ecom_sales.groupby(['Year-Month'])['OrderValue'].sum().tolist())
app = dash.Dash()
app.layout = html.Div([html.H1('Plotly dashboards'),
                       html.H2('Plot of purchase OrderValue for each month'),
                       dcc.Graph(id='fig_1', figure=fig1),
                       html.Br(),
                       # dcc.Graph(id='fig', figure=fig),
                       html.Br(),
                       html.H2('Interactive dropdown dashboard'),
                       dcc.Dropdown(id="dropdown_value", options=['Quantity', 'OrderValue', 'UnitPrice'],
                                    value='OrderValue',
                                    multi=False),
                       html.P(id='dropdown_text', children=[]),
                       dcc.Graph(id='fig_2', figure={})])


@app.callback(
    [Output(component_id='dropdown_text', component_property='children'),
     Output(component_id='fig_2', component_property='figure')],
    [Input(component_id="dropdown_value", component_property='value')]
)
def update_figures(field_inp_value):
    column_input_container = "Column to analyse for each country {}".format(field_inp_value)
    # order_val = ecom_sales.groupby(['Year-Month'])['OrderValue'].agg('count').reset_index().loc[inp_value]
    if field_inp_value == "Quantity":
        x = ecom_sales.groupby(['Country'])[field_inp_value].sum().index
        y = ecom_sales.groupby(['Country'])[field_inp_value].sum().tolist()
        title="Sum '{}' for each country".format(field_inp_value)
    else:
        x = ecom_sales.groupby(['Country'])[field_inp_value].mean().index
        y = ecom_sales.groupby(['Country'])[field_inp_value].mean().tolist()
        title = "Average '{}' for each country".format(field_inp_value)
    fig2 = px.bar(x=x, y=y, title=title)
    fig2.update_xaxes(title_text='Country', tickangle=90)
    fig2.update_yaxes(title_text=title)
    return column_input_container, fig2


if __name__ == '__main__':
    app.run_server(debug=True)
