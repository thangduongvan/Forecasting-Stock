import datetime
import pandas_datareader.data as web
import dash
import pandas


#read historical data
df = pandas.read_csv('D:/NY Exchange/application/data/prices.csv')

#get stock symbols from historical data
id = df['symbol'].unique()
#read data from https://stooq.com/
start = datetime.datetime(2021, 1, 1)
end = datetime.datetime(2021, 12, 3)
df1 = web.DataReader(id[:5], 'stooq', start=start, end=end)


#create style sheets
external_stylesheets = [
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x',
        'crossorigin': 'anonymous'
    },
    {
        'href': 'https://unpkg.com/aos@next/dist/aos.css',
        'rel': 'stylesheet'
    },
    {
        'href': "D:/NY Exchange/application/dash-project/static/main.css",
        'rel': 'stylesheet',
        'type': 'text/css'
    }
]

#create dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = app.server