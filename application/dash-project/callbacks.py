from dash.dependencies import Input, Output, State, ALL
import plotly.express as px
from dash import dcc
import dash_bootstrap_components as dbc
import time
from app import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
import numpy as np

#split data to sequence for training model
def split_sequences(sequence, n_input, n_output):
    X, y = list(), list()
    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + n_input
        out_end_ix = end_ix + n_output
        # check if we are beyond the sequence
        if out_end_ix > len(sequence):
            break
        # gather input and output parts of the pattern
        # the data looks like [[open, close, low, high]] so [0][1] is the close value
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix:out_end_ix][0][1]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

#train the model
def build_model(train, n_input, numnodes, n_output, n_features=4):
    # define parameters
    verbose, epochs = 0, 200
    # prepare data
    train_x, train_y = split_sequences(train, n_input, n_output)
    # reshape the data
    train_x = train_x.reshape((train_x.shape[0], train_x.shape[1], n_features))
    # define model
    model = Sequential()
    model.add(LSTM(numnodes, activation='relu', input_shape=(n_input, n_features)))
    model.add(Dense(n_output))
    model.compile(optimizer='Adamax', loss='mse')
    # fit network
    model.fit(train_x, train_y, epochs=200, verbose=verbose)
    return model

#forecasting
def forecast(model, history, n_input, n_features=4):
    # retrieve last observations for input data
    input_x = np.array(history[-n_input:])
    # reshape into [1, n_input, 1]
    input_x = input_x.reshape((1, len(input_x), n_features))
    # forecast
    yhat = model.predict(input_x, verbose=0)
    # we only want the vector forecast
    yhat = yhat[0]
    return yhat

#callback function for historical data page
@app.callback(
    [Output('line-fig', 'figure'),
     Output('line-fig1', 'figure')],
    [Input('my-dpdn', 'value'),
     Input('my-dpdn1', 'value')]
)
def update_graph(stock_slctd, stock_slctd1):
    dff = df[df['symbol']==stock_slctd]
    figln = px.line(dff, x='date', y='close')
    dff1 = df[df['symbol'].isin(stock_slctd1)]
    figln1 = px.line(dff1, x='date', y='close', color='symbol')
    return figln, figln1

#callback function for update data page
@app.callback(
    [Output('line-fig2', 'figure'),
     Output('line-fig3', 'figure'),
     Output('alert', 'children')],
    [Input('my-dpdn2', 'value'),
     Input('my-dpdn3', 'value')]
)
def update_graph(stock_slctd2, stock_slctd3):
    if df1.empty:
        alert = dbc.Alert("Exceeded daily limit of downloads from stooq",
                          color="danger", dismissable="True")
        return dash.no_update, dash.no_update, alert
    dff2 = df1[df1['Symbols']==stock_slctd2]
    figln2 = px.line(dff2, x='date', y='close')
    dff3 = df1[df1['Symbols'].isin(stock_slctd3)]
    figln3 = px.line(dff3, x='date', y='close', color='symbol')
    return figln2, figln3, dash.no_update

#callback function for forecasting stock page
@app.callback(
    Output('dropdown-container', 'children'),
    Input('dropdown-input', 'value'),
    State('dropdown-container', 'children'))
def display_dropdowns(value, children):
    children = []
    for i in range(1, int(value) +1):
        new_dropdown = dbc.Row([
            dbc.Col('Day '+str(i)+':'),
            dbc.Col(
                dcc.Input(
                    id={
                        'type': 'input',
                        'index': i
                    },
                    type='number',
                    placeholder="input type number"
                ),
            ),
            dbc.Col(
                dcc.Input(
                    id={
                        'type': 'input',
                        'index': i
                    },
                    type='number',
                    placeholder="input type number"
                ),
            ),
            dbc.Col(
                dcc.Input(
                    id={
                        'type': 'input',
                        'index': i
                    },
                    type='number',
                    placeholder="input type number"
                ),
            ),
            dbc.Col(
                dcc.Input(
                    id={
                        'type': 'input',
                        'index': i
                    },
                    type='number',
                    placeholder="input type number"
                )
            )

        ])
        children.append(new_dropdown)
    return children

@app.callback(
    Output("loading-output-1", "children"),
    Input('submit-val', 'n_clicks'),
    State({'type': 'input', 'index': ALL}, 'value'),
    State('line-fig4', 'figure'),
)
def input_triggers_spinner(value, values, fig):
    if fig != {}: return []
    for (i, value) in enumerate(values):
        if value == None:
            return dash.no_update
    if(value > 0):
        time.sleep(30)

@app.callback(
    Output("the_note", "children"),
    Input('submit-val', 'n_clicks'),
    State({'type': 'input', 'index': ALL}, 'value'),
    State('line-fig4', 'figure'),
)
def input_triggers_spinner(value, values, fig):
    if fig != {}: return {}
    for (i, value) in enumerate(values):
        if value == None:
            return {}
    if(value > 0):
        alert = dbc.Alert("The application is running, please wait!", color="primary", dismissable="False", duration=30000)
        return alert

@app.callback(
    [Output('line-fig4', 'figure'),
     Output("the_alert", "children")],
    Input('submit-val', 'n_clicks'),
    State({'type': 'input', 'index': ALL}, 'value'),
    State('dropdown-input', 'value'),
    State('dropdown-input1', 'value'),
    State('my-dpdn4', 'value')
)

def display_output(n_clicks, values, n_input, n_output, symbol):
    if n_clicks == 0:
        return dash.no_update, dash.no_update
    dt = df[df.symbol == symbol]
    dt.drop(['date'], 1, inplace=True)
    dt.drop(['symbol'], 1, inplace=True)
    dt.drop(['volume'], 1, inplace=True)
    input = []
    result = []
    count = 0
    for (i, value) in enumerate(values):
        if value == None:
            alert = dbc.Alert("Please fill all input number!", color="danger", dismissable="False", duration=3000)
            return dash.no_update, alert
        input.append(float(value))
        if (i + 1) % 2 == 0 and (i + 1) % 4 != 0:
            count += 1
            result.append(float(value))
    n_input = int(n_input)
    n_output= int(n_output)
    numnodes = 200
    history = []
    for i in dt.index:
        history.append(dt.loc[i].values)
    model = build_model(history, n_input, numnodes, n_output)
    input = np.array(input)
    input = input.reshape((1, n_input, 4))
    # forecast
    yhat = model.predict(input, verbose=0)
    # we only want the vector forecast
    yhat = yhat[0]
    for value in yhat:
        result.append(value)
    temp = []
    for i in range(len(result)):
        if i == count:
            temp.append([result[i], i, 'input'])
        if i < count:
            temp.append([result[i], i, 'input'])
        else:
            temp.append([result[i], i, 'output'])
    temp = pandas.DataFrame(temp, columns=['close', 'date', 'type'])
    fig = px.line(temp, x = 'date', y = 'close', color='type')
    return fig, dash.no_update