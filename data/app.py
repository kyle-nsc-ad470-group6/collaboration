# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import numpy as np

# Incorporate data
df = pd.read_csv('Seattle_Pet_Licenses.csv')
df = df[~df['Species'].isin(['Goat', 'Pig'])]
df['DATETIME'] = pd.to_datetime(df['License Issue Date'])
df['MONTH'] = df['DATETIME'].dt.month
df['YEAR'] = df['DATETIME'].dt.year

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.RadioItems(options=['2021', '2022', '2023'], value='2023', id='year-control-radio-item'),
    dcc.Graph(figure={}, id='controls-and-graph')
])

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='year-control-radio-item', component_property='value')
)

def update_graph(year_selected=2021):
    df_table = df[df['YEAR'] == int(year_selected)]
    table = df_table.pivot_table(index='MONTH', columns='Species', values='License Number', aggfunc=np.count_nonzero)
    table['MONTH'] = table.index
    fig = px.bar(table, x='MONTH', y=['Dog', 'Cat'], title='Monthly Registrations')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
