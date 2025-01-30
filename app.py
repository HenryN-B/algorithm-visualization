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
import greedy_triangulation as gt
import delaunay as d
import Incremental as ncr

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
    hull, pts, num = gs.graham_scan(set)
    start_time = time.perf_counter()
    temp = gs.gs_complete(set)
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

def greedy(set):
    start_time = time.perf_counter()
    greedy = gt.greedyTriangulationAlgorithm(set)
    end_time = time.perf_counter()
    total_time = end_time-start_time

    return greedy, total_time

def delaunay(set):
    start_time = time.perf_counter()
    gram_tri, del_tri, hull = d.triangulate(set)
    end_time = time.perf_counter()
    total_time = end_time-start_time

    return del_tri, total_time, hull

def incremental(set):
    start_time = time.perf_counter()
    hull_inc = ncr.incr(set)
    end_time = time.perf_counter()
    total_time = end_time-start_time
    # hull_inc = nh.sort_points_counterclockwise(hull_inc)
    x = []
    y = []
    for i in hull_inc:
        x.append(i[0])
        y.append(i[1])
    x.append(hull_inc[0][0])
    y.append(hull_inc[0][1])
    pX = []
    pY = []
    for i in set:
        pX.append(i[0])
        pY.append(i[1])
    return hull_inc, total_time, x, y, pX, pY
    


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
fig.update_layout(showlegend=False)

hull_naive, total_time2, x2, y2, pX2, pY2 = incremental(set)

fig3 = px.imshow(np.zeros(shape=(120, 120, 4)), origin='lower')
fig3.add_scatter(x=x2, y=y2, mode='lines+markers',marker_color='white',marker_size=8)
fig3.add_scatter(x=pX2, y=pY2, mode='markers',marker_color='white',marker_size=4)

# update layout
fig3.update_layout(
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
fig3.update_coloraxes(showscale=False)
fig3.update_layout(showlegend=False)

hull_naive, total_time2, x2, y2, pX2, pY2 = naive(set)

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
fig2.update_layout(showlegend=False)






#greedy 
greedy_tri, total_time4 = greedy(set)
greedy_weight = gt.totalEdgeLength(greedy_tri)
fig4 = px.imshow(np.zeros(shape=(120, 120, 4)), origin='lower')
for line in greedy_tri:
    x = [line[0][0],line[1][0]]
    y = [line[0][1],line[1][1]]
    fig4.add_scatter(x=x, y=y, mode='lines+markers',marker_color='white',marker_size=8)
fig4.update_layout(
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
fig4.update_coloraxes(showscale=False)
fig4.update_layout(showlegend=False)


del_tri, total_time5, hull = delaunay(set)
del_weight = d.totalEdgeLength(del_tri,hull)
fig5 = px.imshow(np.zeros(shape=(120, 120, 4)), origin='lower')
for triangle in del_tri:
    x = [triangle[0][0],triangle[1][0],triangle[2][0]]
    y = [triangle[0][1],triangle[1][1],triangle[2][1]]
    fig5.add_scatter(x=x, y=y, mode='lines+markers',marker_color='white',marker_size=8)
    
x = []
y = []
for point in hull:
    x.append(point[0])
    y.append(point[1])
fig5.add_scatter(x=x, y=y, mode='lines+markers',marker_color='white',marker_size=8)
fig5.update_layout(
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
fig5.update_coloraxes(showscale=False)
fig5.update_layout(showlegend=False)

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
                ),
                dbc.Col(
                    [   
                        html.P(
                            "Incremental Hull",
                            style={
                                'fontSize': '30px'
                            }
                            
                        ),
                        # really cool graph
                        dcc.Graph(
                            id='graph-3',  
                            figure=fig3,
                            config={
                                'scrollZoom': True,
                                'displayModeBar': False,
                            }
                        ),
                        # Button
                        dbc.Button(
                            "Re-run with New Points",
                            id='rerun-button-inc', 
                            color='primary',
                            n_clicks=0
                        ),
                        dbc.Button(
                            "Next",
                            id='next-button-inc',
                            color='primary',
                            n_clicks=0
                        ),
                        # Runtime 
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.P(
                                        id="runtime-text-inc",  
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
                            "Greedy triangulation",
                            style={
                                'fontSize': '30px'
                            }
                            
                        ),
                        # really cool graph
                        dcc.Graph(
                            id='graph-4',  
                            figure=fig4,
                            config={
                                'scrollZoom': True,
                                'displayModeBar': False,
                            }
                        ),
                        # Button
                        dbc.Button(
                            "Re-run with New Points",
                            id='rerun-button-greedy', 
                            color='primary',
                            n_clicks=0
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.P(
                                        id="weight-greedy",  
                                        children=f"Weight {greedy_weight:.0f}",
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
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.P(
                                        id="runtime-text-greedy",  
                                        children=f"Runtime: {total_time4 * 1000:.4f} ms",
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
                ),
                    dbc.Col(
                    [
                        html.P(
                            "Delaunay triangulation",
                            style={
                                'fontSize': '30px'
                            }
                            
                        ),
                        # really cool graph
                        dcc.Graph(
                            id='graph-5',  
                            figure=fig5,
                            config={
                                'scrollZoom': True,
                                'displayModeBar': False,
                            }
                        ),
                        # Button
                        dbc.Button(
                            "Re-run with New Points",
                            id='rerun-button-del', 
                            color='primary',
                            n_clicks=0
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.P(
                                        id="weight-del",  
                                        children=f"Weight {del_weight:.0f}",
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
                        # Runtime 
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.P(
                                        id="runtime-text-del",  
                                        children=f"Runtime: {total_time5 * 1000:.4f} ms",
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
    fig.update_layout(showlegend=False)
    
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
    fig.update_layout(showlegend=False)
    
    runtime_text = f"Runtime: {total_time * 1000:.4f} ms"
    
    return fig, runtime_text

@app.callback(
    [Output('graph-3', 'figure'),
     Output('runtime-text-inc', 'children')],
    Input('rerun-button-inc', 'n_clicks'),
    prevent_initial_call=True
)
def rerun_inc(n_clicks):
    set = gs.random_points(10, 100)
    hull_inc, total_time, x, y, pX, pY = incremental(set)
    
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
    fig.update_layout(showlegend=False)
    
    runtime_text = f"Runtime: {total_time * 1000:.4f} ms"
    
    return fig, runtime_text


@app.callback(
    [Output('graph-4', 'figure'),
     Output('runtime-text-greedy', 'children'),
     Output('weight-greedy','children')],
    Input('rerun-button-greedy', 'n_clicks'),
    prevent_initial_call=True
)
def rerun_greedy(n_clicks):
    set4 = gs.random_points(100,100)
    greedy_tri, total_time = greedy(set4)
    greedy_weight = gt.totalEdgeLength(greedy_tri)

    fig = px.imshow(np.zeros(shape=(120, 120, 4)), origin='lower')

    for line in greedy_tri:
        x = [line[0][0],line[1][0]]
        y = [line[0][1],line[1][1]]
        fig.add_scatter(x=x, y=y, mode='lines+markers',marker_color='white',marker_size=8)

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

    fig.update_coloraxes(showscale=False)
    fig.update_layout(showlegend=False)
    
    runtime_text = f"Runtime: {total_time * 1000:.4f} ms"
    weight_text = f"Runtime: {greedy_weight:.0f}"
    
    return fig, runtime_text, weight_text

@app.callback(
    [Output('graph-5', 'figure'),
     Output('runtime-text-del', 'children'),
     Output('weight-del', 'children')],
    Input('rerun-button-del', 'n_clicks'),
    prevent_initial_call=True
)
def rerun_del(n_clicks):
    set5 = gs.random_points(100,100)
    del_tri, total_time5,hull = delaunay(set5)
    del_weight = d.totalEdgeLength(del_tri,hull)
    fig = px.imshow(np.zeros(shape=(120, 120, 4)), origin='lower')
    for triangle in del_tri:
        x = [triangle[0][0],triangle[1][0],triangle[2][0]]
        y = [triangle[0][1],triangle[1][1],triangle[2][1]]
        fig.add_scatter(x=x, y=y, mode='lines+markers',marker_color='white',marker_size=8)
    x = []
    y = []
    for point in hull:
        x.append(point[0])
        y.append(point[1])
    fig.add_scatter(x=x, y=y, mode='lines+markers',marker_color='white',marker_size=8)


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

    fig.update_coloraxes(showscale=False)
    fig.update_layout(showlegend=False)
    
    runtime_text = f"Runtime: {total_time5 * 1000:.4f} ms"
    weight_text = f"Runtime: {del_weight:.0f}"
    
    return fig, runtime_text, weight_text


if __name__ == '__main__':
    app.run_server(debug=True, port=8053)
