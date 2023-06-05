# Import packages
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Incorporate data
df = pd.read_csv('Seattle_Pet_Licenses.csv')
df = df[~df['Species'].isin(['Goat', 'Pig'])]
df['DATETIME'] = pd.to_datetime(df['License Issue Date'])
df['MONTH'] = df['DATETIME'].dt.month
df['YEAR'] = df['DATETIME'].dt.year
years = df['YEAR'].drop_duplicates().sort_values(ascending=True).values


# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    dcc.Dropdown(['Cat', 'Dog'], value='Dog', id='species-dropdown'),
    dcc.Graph(figure={}, id='top-breed-plot'),
    dcc.Slider(0, 15, 1, value= 10, id='range-top-breeds'),
    html.Hr(),
    dcc.Graph(figure={}, id='pet-registrations-plot'),
    dcc.Checklist(years, [years[-1]], inline=True, id='registration-year-checklist'),
    dcc.RangeSlider(1, 12, 1, value=[1, 12], id='pet-registration-slider')
])

# top breed 
@callback(
    Output(component_id='top-breed-plot', component_property='figure'),
    Input(component_id='species-dropdown', component_property='value'),
    Input(component_id='range-top-breeds', component_property='value')
)
def set_species(selected_species, top_species_count):
    df_species = df[df['Species'] == selected_species]
    df_range = df_species['Primary Breed'].value_counts().sort_values(ascending=False).head(top_species_count)
    fig = px.bar(df_range, x=df_range.values)
    return fig

# registration
@callback(
    Output(component_id='pet-registrations-plot', component_property='figure'),
    Input(component_id='registration-year-checklist', component_property='value'),
    Input(component_id='pet-registration-slider', component_property='value')
)
def plot_registration(years, months):
    months = [i for i in range(months[0], months[1]+1)]
    df_plot = df[df['YEAR'].isin(years)]
    df_plot = df_plot[df_plot['MONTH'].isin(months)]

    df_cat = df_plot[df_plot['Species'] == 'Cat']
    df_cat = df_cat.pivot_table(index='MONTH', values='License Number', columns='Species', aggfunc=np.count_nonzero)
    df_dog = df_plot[df_plot['Species'] == 'Dog']
    df_dog = df_dog.pivot_table(index='MONTH', values='License Number', columns='Species', aggfunc=np.count_nonzero)

    fig = go.Figure(data=[
        go.Bar(name='Cat', x=months, y = df_cat['Cat'].values),
        go.Bar(name='Dog', x=months, y = df_dog['Dog'].values)
    ])
    return fig




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
