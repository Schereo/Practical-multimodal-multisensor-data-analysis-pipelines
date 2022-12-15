# example dash app

import dashboard
from dashboard import html, dcc, Output, Input
import plotly.express as px
import seaborn as sns

iris = sns.load_dataset('iris')

# create dataframe from iris
df = px.data.iris()
# plotly express scatter plot
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", size='petal_length', hover_data=['petal_width'])


app = dashboard.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    dcc.Dropdown(
        id='dropdown',
        options=['sepal_width', 'sepal_length', 'petal_length', 'petal_width'],
        value=['sepal_width', 'sepal_length'],
        multi=True
    ),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),x

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    Input(component_id='dropdown', component_property='value')
)
def update_graph(value):
    fig = px.scatter_matrix(iris, dimensions=value, color="species")
    return fig

# run the dash server
if __name__ == '__main__':
    app.run_server(debug=True)