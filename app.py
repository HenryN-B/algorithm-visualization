import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Sample data
values1 = np.random.randint(10, 100, size=100)
values2 = np.random.randint(10, 100, size=100)

# App layout
app.layout = html.Div([
    dcc.Graph(id='scatter-plot'),
    dcc.Store(id='bar-data', data={'values1': list(values1), 'values2': list(values2)})
])

# Client-side callback (JavaScript function)
app.clientside_callback(
    """
    function(chartType, data) {
        var values1 = data.values1;
        var values2 = data.values2;

        var barmode = chartType === 'scatter';

        return {
            'data': [
                {
                    'x': values1,
                    'y': values2,
                    'type': 'point',
                    'name': 'Series 1'
                },
            ],
            'layout': {
                'title': `Scatterplot (${chartType === 'scatter'})`,
            }
        };
    }
    """,
    Output('scatter-plot', 'figure'),
    [Input('bar-data', 'data')]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)
