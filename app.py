import os
from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
from dash.exceptions import PreventUpdate
import requests
from dotenv import load_dotenv
import pandas as pd
from dateutil import parser
import plotly.graph_objects as go
from plotly.graph_objs import Layout


load_dotenv()
API_KEY = os.getenv("API_KEY")
layout = {
    "paper_bgcolor": "rgb(31, 41, 46)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font_color": "rgb(255, 255, 255)",
    "font": {
        "family": "Courier New, monospace",
        "size": 14,
        "color": "#fff",
    },
}

app = Dash(__name__)


def generate_candlestick_chart(df):
    layout = Layout(
        paper_bgcolor="rgb(31, 41, 46)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="rgb(255, 255, 255)",
        font={"family": "Courier New, monospace", "size": 14, "color": "#fff"},
    )
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
            )
        ],
        layout=layout,
    )

    return fig


class Controller:
    def __init__(self):
        self.function = None
        self.symbol = None
        self.interval = None
        self.api_key = None
        self.adjusted = None
        self.compact = None
        self.data = None
        self.window = None

    def get_data(self):
        if self.adjusted:
            adjusted = "true"
        else:
            adjusted = "false"

        if self.compact:
            compact = "compact"
        else:
            compact = "full"

        url = f"https://www.alphavantage.co/query?function={self.function}&symbol={self.symbol}&interval={self.interval}min&apikey={self.api_key}&adjusted={adjusted}&outputsize={compact}"
        print(url)
        r = requests.get(url)
        data = r.json()
        self.data = self.preprocess_data(data)

    def preprocess_data(self, df):
        df = pd.DataFrame.from_dict(df["Time Series (5min)"], orient="index")
        df = df.rename(
            columns={
                "1. open": "open",
                "2. high": "high",
                "3. low": "low",
                "4. close": "close",
                "5. volume": "vloume",
            }
        )

        for col in df.columns:
            df[col] = pd.to_numeric(df[col])

        df_index = df.index.map(lambda x: parser.parse(x))
        df.index = df_index
        return df

    def __str__(self):
        return f"Class::Controller\nfunction::{self.function}\nsymbol::{self.symbol}\ninterval::{self.interval}\nadjusted::{self.adjusted}\noutputsize::{self.compact}\nwindow::{self.window}"


app_controller = Controller()
app_controller.api_key = API_KEY

app.layout = html.Div(
    className="app-container",
    children=[
        html.Div(
            className="right-slider",
            children=[
                html.H6("Function"),
                dcc.Dropdown(
                    [
                        {"label": "Intraday", "value": "TIME_SERIES_INTRADAY"},
                        {"label": "Daily", "value": "TIME_SERIES_DAILY_ADJUSTED"},
                        {"label": "Weekly", "value": "TIME_SERIES_WEEKLY"},
                    ],
                    "TIME_SERIES_INTRADAY",
                    id="function-dropdown",
                ),
                html.H6("Symbol"),
                dcc.Dropdown(
                    [
                        {"label": "IBM", "value": "IBM"},
                        {"label": "Google", "value": "GOOG"},
                        {"label": "Tesla", "value": "TSLA"},
                    ],
                    "IBM",
                    id="symbol-dropdown",
                ),
                html.H6("Time Interval"),
                dcc.Slider(
                    step=None,
                    marks={1: "1", 5: "5", 15: "15min", 30: "30min", 60: "60min"},
                    value=5,
                    id="time-interval-slider",
                ),
                html.H6("Adjusted"),
                daq.BooleanSwitch(on=True, color="#9B51E0", id="adjusted-switch"),
                html.H6("Compact"),
                daq.BooleanSwitch(on=True, color="#9B51E0", id="compact-switch"),
                html.H6("Window"),
                dcc.Slider(5, 20, 5, value=10, id="window-slider"),
                html.Button("Get", id="get-data"),
            ],
        ),
        html.Div(
            className="main",
            children=[
                html.Div(id="out1"),
                html.Div(id="out2"),
                # dcc.Graph(id="candle-candlestick-graph"),
                dcc.Graph(
                    figure={"layout": layout},
                    id="candle-candlestick-graph",
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("out1", "children"),
    Input("function-dropdown", "value"),
    Input("symbol-dropdown", "value"),
    Input("time-interval-slider", "value"),
    Input("adjusted-switch", "on"),
    Input("compact-switch", "on"),
    Input("window-slider", "value"),
)
def set_app_controller_params(function, symbol, interval, adjusted, compact, window):
    app_controller.function = function
    app_controller.symbol = symbol
    app_controller.interval = interval
    app_controller.adjusted = adjusted
    app_controller.compact = compact
    app_controller.window = window

    return app_controller.__str__()


@app.callback(
    Output("candle-candlestick-graph", "figure"),
    Input("get-data", "n_clicks"),
)
def get_data(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    app_controller.get_data()

    return generate_candlestick_chart(app_controller.data)


if __name__ == "__main__":
    app.run_server(debug=True)
