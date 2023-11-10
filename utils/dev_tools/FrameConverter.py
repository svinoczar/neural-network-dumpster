import pandas as pd
import numpy as np

class FrameConverter:
    frames_for_15m = {"15m":1, "30m":2, "h":4, "4h":16, "12h":48, "d":96, "w":672, "m":2880}

    def binanceConvert(time_frame, path_to_df, save_to_csv=False):
        cdf = pd.read_csv(path_to_df).copy()
        cdf['Date'] = pd.to_datetime(cdf['Date'])
        cdf.set_index('Date', inplace=True)

        resampled_df = cdf.resample(time_frame).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
            'Close Time': 'last',
            'Quote Asset Volume': 'sum',
            'Number of Trades': 'sum',
            'Taker Buy Base Asset Volume': 'sum',
            'Taker Buy Quote Asset Volume': 'sum'
        })
        if save_to_csv :
            with open(f"binance-bitcoin-{time_frame}.csv", "w") as file:
                file.write(resampled_df.reset_index()).to_csv()
        else:
            return resampled_df.reset_index()