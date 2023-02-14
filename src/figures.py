from plotly.graph_objs import Layout
import plotly.graph_objects as go
from darts.models.filtering.moving_average import MovingAverage


def generate_candlestick_chart(df):
    layout = Layout(
        paper_bgcolor="rgba(0,0,0,0)",
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


def generate_time_series_plot(ts, window, label):
    layout = Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="rgb(255, 255, 255)",
        font={"family": "Courier New, monospace", "size": 14, "color": "#fff"},
    )
    print(ts)
    df = ts[window:].pd_dataframe()

    ts_moving_average_7 = MovingAverage(window=7)
    ma_7 = ts_moving_average_7.filter(ts)
    ma_7_df = ma_7[window:].pd_dataframe()

    ts_moving_average_28 = MovingAverage(window=28)
    ma_28 = ts_moving_average_28.filter(ts)
    ma_28_df = ma_28[window:].pd_dataframe()

    # Create traces
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Scatter(x=df.index, y=df.iloc[:, 0], mode="lines", name="lines"))
    fig.add_trace(
        go.Scatter(x=ma_7_df.index, y=ma_7_df.iloc[:, 0], mode="lines", name="lines")
    )
    fig.add_trace(
        go.Scatter(x=ma_28_df.index, y=ma_28_df.iloc[:, 0], mode="lines", name="lines")
    )

    return fig
