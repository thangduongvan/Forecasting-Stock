from dash.dependencies import Input, Output
from layouts import *

#set app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#display layout from path name
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/home':
         return home_layout
    elif pathname == '/historical':
         return hist_layout
    elif pathname == '/update':
         return update_layout
    elif pathname == '/forecast':
         return forecast_layout
    else:
        return home_layout

#run the application
if __name__ == '__main__':
    app.run_server(debug=True)