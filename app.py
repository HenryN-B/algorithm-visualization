import json
import random
import math
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, callback_context, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import numpy as np
import gram_scan as gs
import time
import naive_hull as nh


total_time = 0
num = 0 
hull = []
pts = []

def graham_scan(set):
    global hull
    global pts
    global num
    global graham_scan_done
    graham_scan_done = False
    start_time = time.perf_counter()
    hull, pts, num = gs.graham_scan(set)
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

def naive(set):
    global hull_naive
    start_time = time.perf_counter()
    hull_naive = nh.naive_hull(set)
    end_time = time.perf_counter()
    total_time = end_time-start_time
    hull_naive = nh.sort_points_counterclockwise(hull_naive)
    x = []
    y = []
    for i in hull_naive:
        x.append(i[0])
        y.append(i[1])
    x.append(hull_naive[0][0])
    y.append(hull_naive[0][1])
    pX = []
    pY = []
    for i in set:
        pX.append(i[0])
        pY.append(i[1])
    return hull_naive, total_time, x, y, pX, pY

def update_graham_scan(set,x,y):
    set.append([x,y])
    start_time = time.perf_counter()
    hull = gs.gs_complete(set)
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
# hull, total_time, x, y, pX, pY = naive(set)

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

set2 = gs.random_points(100,100)
hull_naive, total_time2, x2, y2, pX2, pY2 = naive(set2)


fig2 = px.imshow(np.zeros(shape=(120, 120, 4)), origin='lower')
fig2.add_scatter(x=x2, y=y2, mode='lines+markers',marker_color='white',marker_size=8)
fig2.add_scatter(x=pX2, y=pY2, mode='markers',marker_color='white',marker_size=4)

# update layout
fig2.update_layout(
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
fig2.update_coloraxes(showscale=False)

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

server = app.server

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [   
                        html.P(
                            "Graham scan",
                            style={
                                'fontSize': '30px'
                            }
                            
                        ),
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
                            n_clicks=0
                        ),
                        dbc.Button(
                            "Next",
                            id='next-button',
                            color='primary',
                            n_clicks=0
                        ),
                        # Runtime 
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.P(
                                        id="runtime-text",  
                                        children=f"Runtime: {total_time * 1000:.4f} ms",
                                        className="card-text",
                                        style={
                                            'textAlign': 'center',  
                                            'fontSize': '20px', 
                                            'padding': "0px"
                                        }
                                    )
                                ],
                                style={
                                    'padding': '0px', 
                                    'width': '250px',
                                    'height': '40px'
                                }
                            ),
                            style={
                                'padding': '0px', 
                                'width': '250px',
                                'height': '40px'
                            }
                        ),
                    ],
                    style={
                        "justify-content": 'space-evenly',
                    }
                ),
                dbc.Col(
                    [
                        html.P(
                            "Naive scan",
                            style={
                                'fontSize': '30px'
                            }
                            
                        ),
                        # really cool graph
                        dcc.Graph(
                            id='graph-2',  
                            figure=fig2,
                            config={
                                'scrollZoom': True,
                                'displayModeBar': False,
                            }
                        ),
                        # Button
                        dbc.Button(
                            "Re-run with New Points",
                            id='rerun-button-naive', 
                            color='primary',
                            n_clicks=0
                        ),
                        # Runtime 
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.P(
                                        id="runtime-text-naive",  
                                        children=f"Runtime: {total_time2 * 1000:.4f} ms",
                                        className="card-text",
                                        style={
                                            'textAlign': 'center',  
                                            'fontSize': '20px', 
                                            'padding': "0px"
                                        }
                                    )
                                ],
                                style={
                                    'padding': '0px', 
                                    'width': '250px',
                                    'height': '40px'
                                }
                            ),
                            style={
                                'padding': '0px', 
                                'width': '250px',
                                'height': '40px'
                            }
                        )
                    ],
                    style={
                        "justify-content": 'space-evenly',
                    }
                )
            ],
            style={
                "justify-content": 'space-evenly',
            }
        )
    ],
    fluid=True,
    style={
        "width": "100%",
        "height": "100vh"
    }
)

@app.callback(
    Output('graph', 'figure', allow_duplicate=True),
    State('graph', 'figure'),
    Input('graph', 'clickData'),
    prevent_initial_call=True
)
def handle_click(graph_figure, clickData):
    global pts
    global graham_scan_done
    if clickData:
        points = clickData.get('points')[0]
        x = points.get('x')
        y = points.get('y')
        newx, newy, pX, pY, total_time = update_graham_scan(pts, x, y)
        graph_figure['data'][1].update(x=newx)
        graph_figure['data'][1].update(y=newy)
        graph_figure['data'][2].update(y=pY)
        graph_figure['data'][2].update(x=pX)
        graham_scan_done = True
    return graph_figure

@app.callback(
    Output('graph', 'figure', allow_duplicate=True),
    State('graph', 'figure'),
    Input('next-button', 'n_clicks'),
    prevent_initial_call=True
)
def handle_next_button(graph_figure, n_clicks):
    global hull
    global pts
    global num
    global graham_scan_done
    if n_clicks:
        if graham_scan_done:
            return graph_figure
        if num == len(pts):
            return graph_figure
        hull, pts, num = gs.next(hull, pts, num)
        newx = []
        newy = []
        for i in hull:
            newx.append(i[0])
            newy.append(i[1])
        newx.append(hull[0][0])
        newy.append(hull[0][1])
        graph_figure['data'][1].update(x=newx)
        graph_figure['data'][1].update(y=newy)
    return graph_figure

@app.callback(
    [Output('graph', 'figure'),
     Output('runtime-text', 'children')],
    Input('rerun-button', 'n_clicks'),
    prevent_initial_call=True
)
def rerun_graham_scan(n_clicks):
    global graham_scan_done
    graham_scan_done = False
    set = gs.random_points(100, 100)
    hull, total_time, x, y, pX, pY = graham_scan(set)
    
    fig = px.imshow(np.zeros(shape=(120, 120, 4)), origin='lower')
    fig.add_scatter(x=x, y=y, mode='lines+markers', marker_color='white', marker_size=8)
    fig.add_scatter(x=pX, y=pY, mode='markers', marker_color='white', marker_size=4)
    
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
    
    fig.update_coloraxes(showscale=False)
    
    runtime_text = f"Runtime: {total_time * 1000:.4f} ms"
    
    return fig, runtime_text


@app.callback(
    [Output('graph-2', 'figure'),
     Output('runtime-text-naive', 'children')],
    Input('rerun-button-naive', 'n_clicks'),
    prevent_initial_call=True
)
def rerun_naive(n_clicks):
    set = gs.random_points(100, 100)
    hull_naive, total_time, x, y, pX, pY = naive(set)
    
    fig = px.imshow(np.zeros(shape=(120, 120, 4)), origin='lower')
    fig.add_scatter(x=x, y=y, mode='lines+markers', marker_color='white', marker_size=8)
    fig.add_scatter(x=pX, y=pY, mode='markers', marker_color='white', marker_size=4)
    
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
    
    fig.update_coloraxes(showscale=False)
    
    runtime_text = f"Runtime: {total_time * 1000:.4f} ms"
    
    return fig, runtime_text


if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
