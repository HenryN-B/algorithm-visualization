import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Sample data
num = 100
range = 100
values = []
for x in range(100):
    values.append([np.random.randint(0, range), np.random.randint(0, range)])

# App layout
app.layout = html.Div([
    dcc.Graph(id='scatter-plot'),
    dcc.Store(id='bar-data', data={'values': list(values)})
])

# Client-side callback (JavaScript function)
app.clientside_callback(
    """
    function(chartType, data) {
        var values = data.values;

        var barmode = chartType === 'scatter';

        return {
            'data': [
                {
                    datasets: [{
                    pointRadius: 4,
                    pointBackgroundColor: "rgba(0,0,255,1)",
                    data: values
                    }]
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
