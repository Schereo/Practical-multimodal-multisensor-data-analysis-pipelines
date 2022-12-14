from dash import Dash, html, dcc, Output, Input
from pandas import DataFrame
import pandas as pd
import plotly.express as px
import seaborn as sns
from clustering.clustering import cluster
from forecasting.dl.train import predict_precip_for_date
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from preprocessing.clean_data import sum_up_to_days


def setup_layout():
    precip_app.layout = html.Div(children=introductory_text()
                                 + create_daily_precipitation_figure()
                                 + create_daily_histogram_figure()
                                 + create_regression()
                                 + create_correlation()
                                 + create_clustering()
                                 + create_dl_forecasting())


def introductory_text():
    heading = html.H1(children='Precipitation Data Dashboard')
    introduction = html.P(children='''
        This is a dashboard for precipitation data of Oldenburg, Berlin, and Munich. This dashboard is created for the course Practical Multimodal Multisensor Data Analysis Pipelines. The data is analyzed in the following steps:
    ''')
    table_of_contents = html.Ul(children=[
        html.Li(children='Daily precipitation'),
        html.Li(children='Daily precipitation histogram'),
        html.Li(children='Regression'),
        html.Li(children='Correlation'),
        html.Li(children='Clustering'),
        html.Li(children='Deep learning forecasting')
    ])
    return [heading, introduction, table_of_contents]


def read_data():
    global oldenburg_df, berlin_df, munich_df
    oldenburg_df = pd.read_csv('data/processed/oldenburg.csv', index_col=0)
    oldenburg_df.index = pd.to_datetime(oldenburg_df.index)
    oldenburg_df = sum_up_to_days(oldenburg_df)
    renamed_oldenburg_df = oldenburg_df.rename(
        columns={'R1': 'Oldenburg'}, inplace=False)
    berlin_df = pd.read_csv('data/processed/berlin.csv', index_col=0)
    berlin_df.index = pd.to_datetime(berlin_df.index)
    berlin_df = sum_up_to_days(berlin_df)
    renamed_berlin_df = berlin_df.rename(
        columns={'R1': 'Berlin'}, inplace=False)
    munich_df = pd.read_csv('data/processed/munich.csv', index_col=0)
    munich_df.index = pd.to_datetime(munich_df.index)
    munich_df = sum_up_to_days(munich_df)
    renamed_munich_df = munich_df.rename(
        columns={'R1': 'Munich'}, inplace=False)

    global combined_df
    combined_df = pd.concat(
        [renamed_oldenburg_df, renamed_berlin_df, renamed_munich_df], axis=1)
    global oldenburg_prediction_df
    oldenburg_prediction_df = pd.read_csv(
        'data/forecasting/lstm_out.csv', index_col=0)
    oldenburg_prediction_df.rename(
        columns={'R1': 'Oldenburg precip.'}, inplace=True)
    oldenburg_prediction_df.index = pd.to_datetime(
        oldenburg_prediction_df.index)
    oldenburg_prediction_df = sum_up_to_days(oldenburg_prediction_df)

    global pearson_correlation_df
    pearson_correlation_df = pd.read_csv(
        'data/correlation/pearson.csv', index_col=0)

    global rolling_pearson_berlin_munich_df, rolling_pearson_berlin_oldenburg_df, rolling_pearson_munich_oldenburg_df
    rolling_pearson_berlin_munich_df = pd.read_csv(
        'data/correlation/rolling_pearson_Berlin_Munich.csv', index_col=0)
    rolling_pearson_berlin_munich_df.index = pd.to_datetime(
        rolling_pearson_berlin_munich_df.index)
    rolling_pearson_berlin_munich_df = rolling_pearson_berlin_munich_df.resample(
        'D').mean()
    rolling_pearson_berlin_oldenburg_df = pd.read_csv(
        'data/correlation/rolling_pearson_Oldenburg_Berlin.csv', index_col=0)
    rolling_pearson_berlin_oldenburg_df.index = pd.to_datetime(
        rolling_pearson_berlin_oldenburg_df.index)
    rolling_pearson_berlin_oldenburg_df = rolling_pearson_berlin_oldenburg_df.resample(
        'D').mean()
    rolling_pearson_munich_oldenburg_df = pd.read_csv(
        'data/correlation/rolling_pearson_Oldenburg_Munich.csv', index_col=0)
    rolling_pearson_munich_oldenburg_df.index = pd.to_datetime(
        rolling_pearson_munich_oldenburg_df.index)
    rolling_pearson_munich_oldenburg_df = rolling_pearson_munich_oldenburg_df.resample(
        'D').mean()

    global optimal_cluster, agglomerative_cluster
    optimal_cluster, agglomerative_cluster = cluster(oldenburg_df)


def create_daily_precipitation_figure():
    heading = html.H2(
        children='Visualization Precipitation Data of Oldenburg, Berlin, and Munich')
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
        figure=px.line(combined_df, x=combined_df.index, y=combined_df.columns, title='Daily Precipitation', labels={
            'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'})
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
            options=[{'label': 'Daily', 'value': 'D'}, {
                'label': 'Monthly', 'value': 'M'}, {'label': 'Yearly', 'value': 'Y'}],
            value='D',
            clearable=False
        )])
    graph = dcc.Graph(
        id='daily-histogram-plot',
        figure=px.histogram(combined_df, x=combined_df.index, y=combined_df.columns, labels={
            'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'})
    )
    return [heading, city_dropdown, resolution_dropdown, graph]


def create_regression():
    heading = html.H2(children='Regression')
    description = html.P(
        children='A linear regression over all years was used to possibly show a linear relationship between time and precipitation. A trend could not be found. The slope was minimal.')
    city_dropdown = html.Div([
        html.P('City'),
        dcc.Dropdown(
            id='linear-reg-dropdown',
            options=['Oldenburg', 'Berlin', 'Munich'],
            value=['Oldenburg', 'Berlin', 'Munich'],
            multi=True,
            clearable=False
        )])
    resolution_dropdown = html.Div([
        html.P('Resolution'),
        dcc.Dropdown(
            id='linear-reg-resolution-dropdown',
            options=[{'label': 'Daily', 'value': 'D'}, {
                'label': 'Monthly', 'value': 'M'}, {'label': 'Yearly', 'value': 'Y'}],
            value='Y',
            clearable=False
        )])
    regression_type_dropdown = html.Div([
        html.P('Regression Type'),
        dcc.Dropdown(
            id='linear-reg-type-dropdown',
            options=[{'label': 'Linear', 'value': 'ols'}, {'label': 'Local Regression', 'value': 'lowess'}, {
                'label': 'Moving Average', 'value': 'rolling'}, {'label': 'Expanding mean', 'value': 'expanding'}],
            value='ols',
            clearable=False
        )])
    rolling_window = html.Div([
        html.P('Rolling Window'),
        dcc.Slider(
            id='rolling-window-slider',
            min=1,
            max=100,
            step=1,
            value=10,
            marks={i: str(i) for i in range(1, 101, 10)},
            disabled=True
        )])
    graph = dcc.Graph(
        id='regression-plot',
        figure=px.scatter(combined_df, x=combined_df.index, y=combined_df.columns, labels={
            'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'}, trendline="ols")
    )
    return [heading, description, city_dropdown, resolution_dropdown, regression_type_dropdown, rolling_window, graph]


def create_correlation():
    heading = html.H2(children='Correlation')
    heading_2 = html.H3(children='Global Pearson Correlation')
    description_1 = html.P(
        children='A global pearson correlation matrix was created to see if there is a correlation between the precipitation of the cities. The correlation between the cities is minimal / not existing.')
    graph_1 = dcc.Graph(
        id='correlation-plot',
        figure=px.imshow(pearson_correlation_df, labels={
            'x': 'City', 'y': 'City', 'color': 'Pearson Correlation'}, text_auto=True)
    )
    heading_3 = html.H3(children='Rolling Pearson Correlation')
    description_2 = html.P(
        children='Also a rolling pearson correlation with a window of 30h was calculated to see if there is a time based correlation between the precipitation of the cities. The correlation between the cities is at specific times close to 1 but rather often close to 0. In comparison to the global pearson correlation the rolling windows correlation is at certain time intervals much more related.')
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        vertical_spacing=0.1)
    fig.add_trace(go.Scatter(x=rolling_pearson_berlin_munich_df.index,
                  y=rolling_pearson_berlin_munich_df['Correlation'], name='Berlin & Munich'), row=1, col=1)
    fig.add_trace(go.Scatter(x=rolling_pearson_berlin_oldenburg_df.index,
                  y=rolling_pearson_berlin_oldenburg_df['Correlation'], name='Berlin & Oldenburg'), row=2, col=1)
    fig.add_trace(go.Scatter(x=rolling_pearson_munich_oldenburg_df.index,
                  y=rolling_pearson_munich_oldenburg_df['Correlation'], name='Munich & Oldenburg'), row=3, col=1)
    fig.update_layout(height=900)
    graph_2 = dcc.Graph(
        id='rolling-correlation-plot',
        figure=fig
    )
    return [heading, description_1, heading_2, graph_1, heading_3, description_2, graph_2]


def create_clustering():
    heading = html.H2(children='Clustering')
    description_1 = html.P(
        children='First a optimal clusters for the seasons where identified manually (spring, summer, autumn, winter). Then the yearly precipitation was clustered into these seasons. The yearly precipitation was clustered into 4 clusters. Than the agglomerative clustering algorithm was used to cluster the same data. The identified clusters matched the manually identified clusters partially. The winter season could not be identified by the algorithm.'
    )
    city_dropdown = html.Div([
        html.P('City'),
        dcc.Dropdown(
            id='cluster-city-dropdown',
            options=['Oldenburg', 'Berlin', 'Munich'],
            value='Oldenburg',
            multi=False,
            clearable=False
        )])
    years = [str(year) for year in range(1999, 2011)]
    clustering_year_dropdown = html.Div([
        html.P('Year'),
        dcc.Dropdown(
            id='cluster-year-dropdown',
            options=[{'label': year, 'value': year} for year in years],
            value=years[0],
            multi=False,
            clearable=False
        )])
    heading_2 = html.H3(children='Optimal Clustering')
    graph_1 = dcc.Graph(
        id='optimal-clustering-plot',
        figure=px.scatter(optimal_cluster, x=optimal_cluster.index, y=optimal_cluster.columns, labels={
            'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'}, color='cluster')
    )
    heading_3 = html.H3(children='Agglomerative Clustering')
    graph_2 = dcc.Graph(
        id='agglomerative-clustering-plot',
        figure=px.scatter(agglomerative_cluster, x=agglomerative_cluster.index, y=agglomerative_cluster.columns, labels={
            'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'}, color='cluster'))
    return [heading, city_dropdown, clustering_year_dropdown, heading_2, description_1, graph_1, heading_3, graph_2]


def create_dl_forecasting():
    heading = html.H2(children='Deep Learning Forecasting')
    description = html.P('A LSTM model was trained to predict the precipitation of the next day based on the precipitation of the last 10 days. The models seems to only predict the average precipitation. A future improvement could be to use the hourly precipitation data to predict the hourly precipitation of the next day.')
    prediction = html.Div([
        html.P('Choose a date to see the predicted precipitation:'),
        dcc.DatePickerSingle(
            id='date-picker',
            initial_visible_month=oldenburg_prediction_df.index[0],
            date=oldenburg_prediction_df.index[0]
        ),
        html.P(id='prediciton-date'),
        html.P(id='prediction')])

    graph = dcc.Graph(
        id='predicted-precipitation-plot',
        figure=px.line(oldenburg_prediction_df, x=oldenburg_prediction_df.index, y=oldenburg_prediction_df.columns, labels={
            'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'})
    )
    return [heading, description, prediction, graph]


combined_df: DataFrame
precip_app = Dash(__name__)
read_data()
setup_layout()


@precip_app.callback(
    Output(component_id='daily-precipitation-plot',
           component_property='figure'),
    Input(component_id='daily-dropdown', component_property='value')
)
def update_daily(value):
    filtered_df = combined_df[value]
    fig = px.line(filtered_df, x=filtered_df.index, y=filtered_df.columns, labels={
                  'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'})
    return fig


@precip_app.callback(
    Output(component_id='daily-histogram-plot', component_property='figure'),
    Input(component_id='histogram-dropdown', component_property='value'),
    Input(component_id='histogram-resolution-dropdown',
          component_property='value')
)
def update_histogram(city, resolution):
    updated_df = combined_df[city].resample(resolution).sum()
    fig = px.histogram(updated_df, x=updated_df.index, y=updated_df.columns,  labels={
                       'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'})
    return fig


@precip_app.callback(
    Output(component_id='regression-plot', component_property='figure'),
    Output(component_id='rolling-window-slider',
           component_property='disabled'),
    Input(component_id='linear-reg-dropdown', component_property='value'),
    Input(component_id='linear-reg-resolution-dropdown',
          component_property='value'),
    Input(component_id='linear-reg-type-dropdown', component_property='value'),
    Input(component_id='rolling-window-slider', component_property='value')
)
def update_regression(city, resolution, regression_type, rolling_window):
    updated_df = combined_df[city].resample(resolution).sum()

    if regression_type == 'rolling':
        fig = px.scatter(updated_df, x=updated_df.index, y=updated_df.columns, labels={
                         'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'}, trendline=regression_type, trendline_options={'window': rolling_window})
        return fig, False
    else:
        fig = px.scatter(updated_df, x=updated_df.index, y=updated_df.columns, labels={
                         'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'}, trendline=regression_type)
        # TODO: Maybe add the trendline results to the graph
        # results = px.get_trendline_results(fig)
        # print(results)
        return fig, True


@precip_app.callback(
    Output(component_id='optimal-clustering-plot',
           component_property='figure'),
    Output(component_id='agglomerative-clustering-plot',
           component_property='figure'),
    Input(component_id='cluster-year-dropdown', component_property='value'),
    Input(component_id='cluster-city-dropdown', component_property='value')
)
def update_clustering(year, city):
    # print('oldenburg_df', oldenburg_df.head())
    if city == 'Oldenburg':
        optimal_cluster, agglomerative_cluster = cluster(oldenburg_df, year)
    elif city == 'Munich':
        optimal_cluster, agglomerative_cluster = cluster(munich_df, year)
    else:
        optimal_cluster, agglomerative_cluster = cluster(berlin_df, year)

    fig_1 = px.scatter(optimal_cluster, x=optimal_cluster.index, y=optimal_cluster.columns, labels={
        'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'}, color='cluster')
    fig_2 = px.scatter(agglomerative_cluster, x=agglomerative_cluster.index, y=agglomerative_cluster.columns, labels={
        'value': 'Precipitation in mm', 'variable': 'City', 'index': 'Date'}, color='cluster')
    return fig_1, fig_2


@precip_app.callback(
    Output(component_id='prediciton-date', component_property='children'),
    Output(component_id='prediction', component_property='children'),
    Input(component_id='date-picker', component_property='date')
)
def update_prediction(date):
    date = pd.to_datetime(date)
    prediciton = predict_precip_for_date(date)
    return f'Prediction for {date.month}/{date.day}/{date.year}: ', f'{prediciton} mm'


precip_app.run_server(debug=True)
