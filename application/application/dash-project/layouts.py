from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from app import *
import callbacks

#layout for home page
home_layout = html.Div([
    html.Nav([
        html.Div([
            html.A([
                "Forecasting NY Stock"
            ],className="navbar-brand", href="/"),
            html.Div([
                html.Ul([
                    html.Li([
                        html.A(["Home"], href="/home", className="nav-link text-white")
                    ], className="nav-item"),
                    html.Li([
                        html.A(["Historical data"], href="/historical", className="nav-link text-white")
                    ], className="nav-item"),
                    html.Li([
                        html.A(["Update data"], href="/update", className="nav-link text-white")
                    ], className="nav-item"),
                    html.Li([
                        html.A(["Forecasting stock"], href="/forecast", className="nav-link text-white")
                    ], className="nav-item")
                ], className="navbar-nav ml-auto mb-2 mb-lg-0")
            ], className="collapse navbar-collapse")
        ], className="container-fluid")
    ], className= "navbar navbar-expand-lg navbar-dark bg-primary"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H1(["New York Stock Exchange"], className = "text-center text-primary mb-4")
                    ], className="site-header-logo"),
                    html.Img(src="https://cdn.corporatefinanceinstitute.com/assets/new-york-stock-exchange.jpeg")
                ], className="ml-auto mr-auto")
            ], className="col-md-12 col-sm-12 col-xm-12")
        ], className="row")
    ], className="container")
])

#layout for historical data page
hist_layout = html.Div([
    html.Nav([
        html.Div([
            html.A([
                "Forecasting NY Stock"
            ],className="navbar-brand", href="/"),
            html.Div([
                html.Ul([
                    html.Li([
                        html.A(["Home"], href="/home", className="nav-link text-white")
                    ], className="nav-item"),
                    html.Li([
                        html.A(["Historical data"], href="/historical", className="nav-link text-white")
                    ], className="nav-item"),
                    html.Li([
                        html.A(["Update data"], href="/update", className="nav-link text-white")
                    ], className="nav-item"),
                    html.Li([
                        html.A(["Forecasting stock"], href="/forecast", className="nav-link text-white")
                    ], className="nav-item")
                ], className="navbar-nav ml-auto mb-2 mb-lg-0")
            ], className="collapse navbar-collapse")
        ], className="container-fluid")
    ], className= "navbar navbar-expand-lg navbar-dark bg-primary"),
    dbc.Container([

        dbc.Row(
            dbc.Col(html.H1("New York Stock Exchange",
                            className='text-center text-primary mb-4'),
                    width=12)
        ),

        dbc.Row([

            dbc.Col([
                dcc.Dropdown(id='my-dpdn', multi=False, value='AMZN',
                             options=[{'label':x, 'value':x}
                                      for x in sorted(df['symbol'].unique())],
                             ),
                dcc.Graph(id='line-fig', figure={})
            ],# width={'size':5, 'offset':1, 'order':1},
               xs=12, sm=12, md=12, lg=5, xl=5
            ),

            dbc.Col([
                dcc.Dropdown(id='my-dpdn1', multi=True, value=['FB'],
                             options=[{'label':x, 'value':x}
                                      for x in sorted(df['symbol'].unique())],
                             ),
                dcc.Graph(id='line-fig1', figure={})
            ], #width={'size':5, 'offset':0, 'order':2},
               xs=12, sm=12, md=12, lg=5, xl=5
            ),

        ], justify='start'),  # Horizontal:start,center,end,between,around

    ], fluid=True)
])

#layout for update data page
update_layout = html.Div([
    html.Nav([
        html.Div([
            html.A([
                "Forecasting NY Stock"
            ],className="navbar-brand", href="/"),
            html.Div([
                html.Ul([
                    html.Li([
                        html.A(["Home"], href="/home", className="nav-link text-white")
                    ], className="nav-item"),
                    html.Li([
                        html.A(["Historical data"], href="/historical", className="nav-link text-white")
                    ], className="nav-item"),
                    html.Li([
                        html.A(["Update data"], href="/update", className="nav-link text-white")
                    ], className="nav-item"),
                    html.Li([
                        html.A(["Forecasting stock"], href="/forecast", className="nav-link text-white")
                    ], className="nav-item")
                ], className="navbar-nav ml-auto mb-2 mb-lg-0")
            ], className="collapse navbar-collapse")
        ], className="container-fluid")
    ], className= "navbar navbar-expand-lg navbar-dark bg-primary"),
    dbc.Container([

        dbc.Row(
            dbc.Col(html.H1("New York Stock Exchange",
                            className='text-center text-primary mb-4'),
                    width=12)
        ),
        html.Div(id="alert", children=[]),
        dbc.Row([

            dbc.Col([
                dcc.Dropdown(id='my-dpdn2', multi=False, value='AMZN',
                             options=[{'label':x, 'value':x}
                                      for x in sorted(df['symbol'].unique())],
                             ),
                dcc.Graph(id='line-fig2', figure={})
            ],# width={'size':5, 'offset':1, 'order':1},
               xs=12, sm=12, md=12, lg=5, xl=5
            ),

            dbc.Col([
                dcc.Dropdown(id='my-dpdn3', multi=True, value=['AMZN'],
                             options=[{'label':x, 'value':x}
                                      for x in sorted(df['symbol'].unique())],
                             ),
                dcc.Graph(id='line-fig3', figure={})
            ], #width={'size':5, 'offset':0, 'order':2},
               xs=12, sm=12, md=12, lg=5, xl=5
            ),

        ], justify='start'),  # Horizontal:start,center,end,between,around

    ], fluid=True)
])

#layout for forecasting stock page
forecast_layout = html.Div([
    html.Nav([
        html.Div([
            html.A([
                "Forecasting NY Stock"
            ],className="navbar-brand", href="/"),
            html.Div([
                html.Ul([
                    html.Li([
                        html.A(["Home"], href="/home", className="nav-link text-white")
                    ], className="nav-item"),
                    html.Li([
                        html.A(["Historical data"], href="/historical", className="nav-link text-white")
                    ], className="nav-item"),
                    html.Li([
                        html.A(["Update data"], href="/update", className="nav-link text-white")
                    ], className="nav-item"),
                    html.Li([
                        html.A(["Forecasting stock"], href="/forecast", className="nav-link text-white")
                    ], className="nav-item")
                ], className="navbar-nav ml-auto mb-2 mb-lg-0")
            ], className="collapse navbar-collapse")
        ], className="container-fluid")
    ], className= "navbar navbar-expand-lg navbar-dark bg-primary"),
    dbc.Container([

        dbc.Row(
            dbc.Col(html.H1("New York Stock Exchange",
                            className='text-center text-primary mb-4'),
                    width=12)
        ),

        dbc.Row([
                dbc.Col(
                    dcc.Dropdown(id='my-dpdn4', multi=False, value='AMZN',
                                 options=[{'label':x, 'value':x}
                                          for x in sorted(df['symbol'].unique())],
                                 )
                ),
                dbc.Col(
                    dcc.Dropdown(id='dropdown-input', multi=False, value='1',
                                 options=[{'label': x, 'value': x}
                                          for x in range(1, 31)],
                                 ),
                ),
            ]),
            html.Br(),
            html.Div(id="the_alert", children=[]),
            dbc.Row(id='dropdown-container', children=[]),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    'Number of forecasted days:'
                ),
                dbc.Col(
                    dcc.Dropdown(id='dropdown-input1', multi=False, value='1',
                                 options=[{'label': x, 'value': x}
                                          for x in range(1, 31)],
                                 ),
                ),
            ]),
            html.Button('Submit', id='submit-val', n_clicks=0),
            html.Div(id="the_note", children=[], className="text-center"),
            dcc.Loading(
                    id="loading-1",
                    type="default",
                    children=html.Div(id="loading-output-1")
                ),
            dcc.Graph(id='line-fig4', figure={})
    ])
])