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



def graham_scan(set):
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
    return hull, total_time, x, y, pX, pY

def update_graham_scan(set,x,y):
    set.append([x,y])
    start_time = time.perf_counter()
    hull = gs.graham_scan(set)
    end_time = time.perf_counter()
    total_time = end_time-start_time
    newx = []
    newy = []
    for i in hull:
        newx.append(i[0])
        newy.append(i[1])
    newx.append(hull[0][0])
    newy.append(hull[0][1])
    pX = []
    pY = []
    for i in set:
        pX.append(i[0])
        pY.append(i[1])
    return newx, newy, pX, pY, total_time



set = gs.random_points(100, 100)
hull, total_time, x, y, pX, pY = graham_scan(set)
fig = px.imshow(np.zeros(shape=(120, 120, 4)), origin='lower')
fig.add_scatter(x=x, y=y, mode='lines+markers',marker_color='white',marker_size=8)
fig.add_scatter(x=pX, y=pY, mode='markers',marker_color='white',marker_size=4)

# update layout
fig.update_layout(
    template='plotly_dark',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    hoverdistance=1,
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

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    # really cool graph
                    dcc.Graph(
                        id='graph',
                        figure=fig,
                        config={
                            'scrollZoom': True,
                            'displayModeBar': False,
                        }
                    ),
                    # Button
                    dbc.Button(
                        "Re-run with New Points",
                        id='rerun-button',
                        color='primary',
                        className='shadow-sm my-3',  
                        n_clicks=0
                    ),
                    # Runtime 
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.P(
                                    f"Runtime: {total_time*1000:.2f} ms",
                                    className="card-text",
                                    style={
                                        'textAlign': 'left',  
                                        'fontSize': '20px'  
                                    }
                                )
                            ]
                        ),
                        className="shadow-sm mt-3", 
                        style={
                            'padding': '5px', 
                            'width': '250px'
                        }
                    )
                ],
                width=8  
            ),
            justify='center',   
        )
    ],
    fluid=True,
    className="px-4 py-3"
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
        newx, newy, pX, pY,total_time = update_graham_scan(set,x,y)
        
        # fig.add_scatter(x=newx, y=newy, mode='lines+markers')
        # update figure data (in this case it's the last trace)
        graph_figure['data'][1].update(x=newx)
        graph_figure['data'][1].update(y=newy)
        graph_figure['data'][2].update(y=pY)
        graph_figure['data'][2].update(x=pX)

    return graph_figure


if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
