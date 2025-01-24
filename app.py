import json
import random
import math
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import numpy as np
import gram_scan as gs
import time


# create image and plotly express object
# fig = px.imshow(
#     np.zeros(shape=(90, 160, 4))
# )
# fig.add_scatter(
#     x=[5, 20, 50],
#     y=[5, 20, 50],
#     mode='markers',
#     marker_color='white',
#     marker_size=10
# )


set = gs.random_points(100, 100)

start_time = time.perf_counter()
hull = gs.graham_scan(set)
end_time = time.perf_counter()
total_time = end_time-start_time
x = []
y = []
for i in hull:
    x.append(i[0])
    y.append(i[1])
x.append(hull[0][0])
y.append(hull[0][1])
pX = []
pY = []
for i in set:
    pX.append(i[0])
    pY.append(i[1])

fig = px.imshow(np.zeros(shape=(100, 100, 4)), origin='lower')
fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers'))
fig.add_trace(go.Scatter(x=pX, y=pY, mode='markers'))

# update layout
fig.update_layout(
    template='plotly_dark',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    width=700,
    height=500,
    margin={
        'l': 0,
        'r': 0,
        't': 20,
        'b': 0,
    }
)

# hide color bar
fig.update_coloraxes(showscale=False)

# Build App
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SLATE],
    meta_tags=[
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'
        }
    ]
)

# app layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id='graph',
                    figure=fig,
                    config={
                        'scrollZoom': True,
                        'displayModeBar': False,
                    }
                ),
                width={'size': 5, 'offset': 0}
            ), justify='around'
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.A(
                            html.Button(
                                'Refresh Page',
                                id='refresh_button'
                            ),
                            href='/'
                        ),
                    ], width={'size': 5, 'offset': 0}
                ),
            ], justify='around'
        ),
        dbc.Row(
            dbc.Col(
                html.Div(
                    id='runtime_display',  
                    children= f"Runtime for Gram Scan: {total_time*1000} milliseconds",
                    style={'textAlign': 'center', 'marginTop': '10px'}
                ),
                width={'size': 5, 'offset': 0}
            ), justify='around'
        )
    ], fluid=True
)


@ app.callback(
    Output('graph', 'figure'),
    State('graph', 'figure'),
    Input('graph', 'clickData')
)
def get_click(graph_figure, clickData):
    if not clickData:
        raise PreventUpdate
    else:
        points = clickData.get('points')[0]
        x = points.get('x')
        y = points.get('y')

        # get scatter trace (in this case it's the last trace)
        scatter_x, scatter_y = [graph_figure['data'][1].get(coords) for coords in ['x', 'y']]
        scatter_x.append(x)
        scatter_y.append(y)

        # update figure data (in this case it's the last trace)
        graph_figure['data'][1].update(x=scatter_x)
        graph_figure['data'][1].update(y=scatter_y)

    return graph_figure


if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
