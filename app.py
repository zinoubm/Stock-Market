from src.constants import *
from src.figures import *
from src.controller import Controller
from src.functions.functions import functions


from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import dash_daq as daq


import plotly.express as px


app = Dash(__name__)


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
                dcc.Markdown(markdown),
                html.H2("Candle Stick Graph"),
                dcc.Graph(
                    className="graph",
                    figure={"layout": layout},
                    id="candlestick-graph",
                ),
                html.H2("Moving Averages"),
                html.Div(
                    className="moving-averages",
                    children=[
                        dcc.Graph(
                            className="moving-average-element graph",
                            figure={"layout": layout},
                            id="moving-average-open-graph",
                        ),
                        dcc.Graph(
                            className="moving-average-element graph",
                            figure={"layout": layout},
                            id="moving-average-high-graph",
                        ),
                        dcc.Graph(
                            className="moving-average-element graph",
                            figure={"layout": layout},
                            id="moving-average-low-graph",
                        ),
                        dcc.Graph(
                            className="moving-average-element graph",
                            figure={"layout": layout},
                            id="moving-average-close-graph",
                        ),
                    ],
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
    app_controller.params["function"] = function
    app_controller.params["symbol"] = symbol
    app_controller.params["interval"] = interval
    app_controller.params["adjusted"] = adjusted
    app_controller.params["compact"] = compact
    app_controller.params["window"] = window
    app_controller.url_handler = functions[function]()

    return app_controller.__str__()


@app.callback(
    [
        Output("candlestick-graph", "figure"),
        Output("moving-average-open-graph", "figure"),
        Output("moving-average-high-graph", "figure"),
        Output("moving-average-low-graph", "figure"),
        Output("moving-average-close-graph", "figure"),
    ],
    [Input("get-data", "n_clicks")],
)
def get_data(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    app_controller.get_data()

    return (
        generate_candlestick_chart(app_controller.data),
        generate_time_series_plot(
            app_controller.series_open, 250, "Open with moving averages"
        ),
        generate_time_series_plot(
            app_controller.series_high, 250, "High with moving averages"
        ),
        generate_time_series_plot(
            app_controller.series_low, 250, "Low with moving averages"
        ),
        generate_time_series_plot(
            app_controller.series_close, 250, "Close with moving averages"
        ),
    )


# Disable Sliders if kernel not in the given list
@app.callback(
    [
        Output("time-interval-slider", "disabled"),
        Output("adjusted-switch", "disabled"),
    ],
    [Input("function-dropdown", "value")],
)
def disable_slider_param_degree(kernel):
    return kernel != "TIME_SERIES_INTRADAY", kernel != "TIME_SERIES_INTRADAY"


if __name__ == "__main__":
    app.run_server(debug=True)
