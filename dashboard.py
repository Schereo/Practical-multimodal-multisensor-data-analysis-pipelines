from dash import Dash, html, dcc, Output, Input
from pandas import DataFrame
import pandas as pd
import plotly.express as px
import seaborn as sns

from preprocessing.clean_data import sum_up_to_days

         
def setup_layout():
    precip_app.layout = html.Div(children=introductory_text()+create_daily_precipitation_figure()+create_daily_histogram_figure()+create_dl_forecasting())

def introductory_text():
    heading = html.H1(children='Precipitation Data Dashboard')
    introduction = html.P(children='''
        This is a dashboard for precipitation data of Oldenburg, Berlin, and Munich. This dashboard is created for the course Practical Multimodal Multisensor Data Analysis Pipelines.
    ''')
    return [heading, introduction]

def read_data():
    oldenburg_df = pd.read_csv('data/processed/oldenburg.csv', index_col=0)
    oldenburg_df.rename(columns={'R1': 'Oldenburg'}, inplace=True)
    oldenburg_df.index = pd.to_datetime(oldenburg_df.index)
    oldenburg_df = sum_up_to_days(oldenburg_df)
    berlin_df = pd.read_csv('data/processed/berlin.csv', index_col=0)
    berlin_df.rename(columns={'R1': 'Berlin'}, inplace=True)
    berlin_df.index = pd.to_datetime(berlin_df.index)
    berlin_df = sum_up_to_days(berlin_df)
    munich_df = pd.read_csv('data/processed/munich.csv', index_col=0)
    munich_df.rename(columns={'R1': 'Munich'}, inplace=True)
    munich_df.index = pd.to_datetime(munich_df.index)
    munich_df = sum_up_to_days(munich_df)
    global combined_df
    combined_df = pd.concat([oldenburg_df, berlin_df, munich_df], axis=1)

def create_daily_precipitation_figure():
    heading = html.H2(children='Visualization Precipitation Data of Oldenburg, Berlin, and Munich')
    dropdown = html.Div([
        html.P('City'),
        dcc.Dropdown(
            id='daily-dropdown',
            options=['Oldenburg', 'Berlin', 'Munich'],
            value=['Oldenburg', 'Berlin', 'Munich'],
            multi=True
        )])
    graph = dcc.Graph(
            id='daily-precipitation-plot',
            figure=px.line(combined_df, x=combined_df.index, y=combined_df.columns, title='Daily Precipitation', labels={'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'})
        )
    return [heading, dropdown, graph]

def create_daily_histogram_figure():
    heading = html.H2(children='Histogram Precipitation Data')

    city_dropdown = html.Div([
        html.P('City'),
        dcc.Dropdown(
            id='histogram-dropdown',
            options=['Oldenburg', 'Berlin', 'Munich'],
            value=['Oldenburg', 'Berlin', 'Munich'],
            multi=True,
            clearable=False
        )])
    resolution_dropdown = html.Div([
        html.P('Resolution'),
        dcc.Dropdown(
            id='histogram-resolution-dropdown',
            options=[{'label': 'Daily', 'value': 'D'}, {'label': 'Monthly', 'value': 'M'}, {'label': 'Yearly', 'value': 'Y'}],
            value='D',
            clearable=False
        )])
    graph = dcc.Graph(
            id='daily-histogram-plot',
            figure=px.histogram(combined_df, x=combined_df.index, y=combined_df.columns, labels={'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'})
        )
    return [heading, city_dropdown, resolution_dropdown, graph]

def create_dl_forecasting():
    heading = html.H2(children='Deep Learning Forecasting')
    return [heading]



combined_df: DataFrame  
precip_app = Dash(__name__)
read_data()
setup_layout()


@precip_app.callback(
    Output(component_id='daily-precipitation-plot', component_property='figure'),
    Input(component_id='daily-dropdown', component_property='value')
)
def update_daily(value):
    filtered_df = combined_df[value]
    fig = px.line(filtered_df, x=filtered_df.index, y=filtered_df.columns, labels={'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'})
    return fig

@precip_app.callback(
    Output(component_id='daily-histogram-plot', component_property='figure'),
    Input(component_id='histogram-dropdown', component_property='value'),
    Input(component_id='histogram-resolution-dropdown', component_property='value')
)
def update_histogram(city, resolution):
    updated_df = combined_df[city].resample(resolution).sum()
    fig = px.histogram(updated_df, x=updated_df.index, y=updated_df.columns,  labels={'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'})
    return fig

precip_app.run_server(debug=True)
    