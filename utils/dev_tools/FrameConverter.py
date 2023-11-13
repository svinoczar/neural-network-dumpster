import pandas as pd
import numpy as np

class FrameConverter:
    # frames_for_1m = {"1m":1, "3m":3, "5m":5, "15m":15, "30m":30, "45m":45, "h":60, "2h":120, "3h":180, "4h":240, "12h":720, "d":1440, "w":10080, "m":43200, "3m":129600, "6m":259200, "12m":518400}
    # frames_for_3m = {"3m":1, "5m":2, "15m":5, "30m":10, "45m":15, "h":20, "2h":40, "3h":60, "4h":80, "12h":240, "d":480, "w":3360, "m":14400}
    # frames_for_5m = {"5m":1, "15m":3, "30m":6, "45m":9, "h":12, "2h":24, "3h":36, "4h":48, "12h":144, "d":288, "w":2016, "m":8640}
    # frames_for_15m = {"15m":1, "30m":2, "45m":3, "h":4, "2h":8, "3h":12, "4h":16, "12h":48, "d":96, "w":672, "m":2880, "3m":8400, "6m":16800, "12m":33600}

    def binanceConvert(time_frame, path_to_df=None, data_frame=None, start_time_frame="15m", save_to_csv=False):
        if path_to_df is None:
            if data_frame is not None:
                cdf = data_frame.copy()
            else:
                print("no path to df and no df. WTF?")
                return 0
        elif path_to_df is not None and data_frame is None:
            cdf = pd.read_csv(path_to_df).copy()
        else:
            print("path to df and df. WTF?")
            return 0
        # frames = frames_for_1m if start_time_frame == "1m" else (frames_for_3m if start_time_frame == "3m" else (frames_for_5m if start_time_frame == "5m" else frames_for_15m))
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
        if save_to_csv:
            file_path = f"binance-bitcoin-{time_frame}.csv"
            resampled_df.reset_index().to_csv(file_path, index=False)
        else:
            return resampled_df.reset_index()