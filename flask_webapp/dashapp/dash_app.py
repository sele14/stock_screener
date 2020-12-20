# Dash App Script

from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html

import yfinance as yf
import matplotlib.pyplot as plt
from newsapi import NewsApiClient

from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import pandas as pd

# Import API key env variable
from env_vars import news_api_key


# path to launch the app
url_base = '/screener/'


# News API key
api_key = news_api_key

# news api callback
def news_api():
    # adding news api
    newsapi = NewsApiClient(api_key=api_key)
    # headlines = newsapi.get_top_headlines(sources='cnbc')

    headlines = newsapi.get_top_headlines(
                                          category='business',
                                          country='us',
                                          language='en')
    articles = headlines['articles']

    news = []
    url = []
    for i in range(len(articles)):
        my_article = articles[i]
        news.append(my_article['title'])  
        url.append(my_article['url'])

    news = pd.DataFrame(news, url)
    news = news.reset_index()
    news.columns = ['URL', 'Article']
    
    return news  

# make a table for the news api data
def news_table(rows=10):
    news_data = news_api()

    return html.Div(
        [
            html.Div(
                html.Table(
                    # Header
                    [html.Tr([html.Th()])]
                    +
                    # Body
                    [
                        html.Tr(
                            [
                                html.Td(
                                    html.A(
                                        news_data.iloc[i]["Article"],
                                        href=news_data.iloc[i]["URL"],
                                        target="_blank"
                                    )
                                )
                            ]
                        )
                        for i in range(min(len(news_data),10))
                    ]
                ),
                style={"height": "300px", "overflowY": "scroll"},
            ),
        ],
        style={"height": "100%"},)



layout = html.Div([

    # User Input Field for Stock Ticker, default = SPY
    html.Div([
        dcc.Input(id="stock-input", value="SPY", type="text"),
        html.Button(id="submit-button", n_clicks=0, children="Submit")
    ]),

    # Main Layout Div
    html.Div([

        # Display Stock Plot
        html.Div([
            dcc.Graph(
                id="graph_close",
            )
        ], className="six columns"),

        # Display Market news feed (to do)
        html.Div([
            html.H3(html.Font("News Feed"),),

            # Display the news from API
            news_table()


        ], className="six columns"),

    ],className="row")
])


### Callbacks ###


def Add_Dash(server):
    dash_app = Dash(server=server, url_base_pathname=url_base)
    apply_layout_with_auth(dash_app, layout)
    dash_app.css.append_css({
    "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
})

    @dash_app.callback(Output('graph_close', 'figure'),
                  [Input("submit-button", "n_clicks")],
                  [State("stock-input", "value")]
                  )

    def update_fig(n_clicks, input_value):
        news_api()
        # API call, grab stock data
        df = yf.Ticker(input_value)
        df = df.history(period="max")

        # df = yf.download(input_value, 
                          # start=start, 
                          # end=end,
                          # interval = '60m',
                          # progress=False)


        trace_line = go.Scatter(x=list(df.index),
                                    y=list(df.Close),
                                    #visible=False,
                                    name="Close",
                                    line={"color":'#005651'},
                                    showlegend=False)

        trace_candle = go.Candlestick(x=df.index,
                               open=df.Open,
                               high=df.High,
                               low=df.Low,
                               close=df.Close,
                               #increasing=dict(line=dict(color="#00ff00")),
                               #decreasing=dict(line=dict(color="white")),
                               visible=False,
                               showlegend=False)

        trace_bar = go.Ohlc(x=df.index,
                               open=df.Open,
                               high=df.High,
                               low=df.Low,
                               close=df.Close,
                               #increasing=dict(line=dict(color="#888888")),
                               #decreasing=dict(line=dict(color="#888888")),
                               visible=False,
                               showlegend=False)

        data = [trace_line, trace_candle, trace_bar]

        updatemenus = list([
            dict(
                buttons=list([
                    dict(
                        args=[{'visible': [True, False, False]}],
                        label='Line',
                        method='update'
                    ),
                    dict(
                        args=[{'visible': [False, True, False]}],
                        label='Candle',
                        method='update'
                    ),
                    dict(
                        args=[{'visible': [False, False, True]}],
                        label='Bar',
                        method='update'
                    ),
                ]),
                direction='down',
                pad={'r': 10, 't': 10},
                showactive=True,
                x=0,
                xanchor='left',
                y=1.05,
                yanchor='top'
            ),
        ])

        layout = dict(
            title=input_value,
            updatemenus=updatemenus,
            autosize=False,
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label='1m',
                             step='month',
                             stepmode='backward'),
                        dict(count=6,
                             label='6m',
                             step='month',
                             stepmode='backward'),
                        dict(count=1,
                             label='YTD',
                             step='year',
                             stepmode='todate'),
                        dict(count=1,
                             label='1y',
                             step='year',
                             stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date'
            )
        )

        return {
            "data": data,
            "layout": layout
        }




    















    return dash_app.server