from darts import TimeSeries
from darts.dataprocessing.transformers import MissingValuesFiller
from darts.dataprocessing.pipeline import Pipeline
import pandas as pd
import numpy as np
from dateutil import parser


class DataManager:
    def __init__(self):
        self.raw_data = None
        self.df = None
        self.series_open = None
        self.series_high = None
        self.series_low = None
        self.series_close = None

    def pipeline(self, data):
        preprocessed_df = self.preprocess_df(data)
        preprocessed_time_series = self.preprocess_time_series(preprocessed_df)
        self.df = preprocessed_df
        self.series_open = preprocessed_time_series["open"]
        self.series_high = preprocessed_time_series["high"]
        self.series_low = preprocessed_time_series["low"]
        self.series_close = preprocessed_time_series["close"]

    def preprocess_df(self, data):
        df = pd.DataFrame.from_dict(data["Time Series (5min)"], orient="index")
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

    def preprocess_time_series(self, df):
        series_open = TimeSeries.from_dataframe(
            df, value_cols="open", fill_missing_dates=True, freq="min"
        )
        series_high = TimeSeries.from_dataframe(
            df, value_cols="high", fill_missing_dates=True, freq="min"
        )
        series_low = TimeSeries.from_dataframe(
            df, value_cols="low", fill_missing_dates=True, freq="min"
        )
        series_close = TimeSeries.from_dataframe(
            df, value_cols="close", fill_missing_dates=True, freq="min"
        )

        ts_filler_open = MissingValuesFiller(verbose=False, n_jobs=-1, name="Fill NAs")
        ts_filler_high = MissingValuesFiller(verbose=False, n_jobs=-1, name="Fill NAs")
        ts_filler_low = MissingValuesFiller(verbose=False, n_jobs=-1, name="Fill NAs")
        ts_filler_close = MissingValuesFiller(verbose=False, n_jobs=-1, name="Fill NAs")

        ts_pipeline_open = Pipeline([ts_filler_open])
        ts_pipeline_high = Pipeline([ts_filler_high])
        ts_pipeline_low = Pipeline([ts_filler_low])
        ts_pipeline_close = Pipeline([ts_filler_close])

        ts_processed_open = ts_pipeline_open.fit_transform(series_open)
        ts_processed_high = ts_pipeline_high.fit_transform(series_high)
        ts_processed_low = ts_pipeline_low.fit_transform(series_low)
        ts_processed_close = ts_pipeline_close.fit_transform(series_close)

        ts_processed_open = ts_processed_open.astype(np.float64)
        ts_processed_high = ts_processed_high.astype(np.float64)
        ts_processed_low = ts_processed_low.astype(np.float64)
        ts_processed_close = ts_processed_close.astype(np.float64)

        return {
            "open": ts_processed_open,
            "high": ts_processed_high,
            "low": ts_processed_low,
            "close": ts_processed_close,
        }
