import os
from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
from dash.exceptions import PreventUpdate
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Dash(__name__)


class Controller:
    def __init__(self):
        self.function = None
        self.symbol = None
        self.interval = None
        self.api_key = None
        self.adjusted = None
        self.compact = None
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
        return data

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
                    value=15,
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
            children=[html.Div(id="out1"), html.Div(id="out2")],
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
    Output("out2", "children"),
    Input("get-data", "n_clicks"),
)
def get_data(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    return app_controller.get_data()


if __name__ == "__main__":
    app.run_server(debug=True)
