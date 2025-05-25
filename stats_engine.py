# stats_engine.py
# Handles the spread calculation, rolling mean, std dev, and Z-score computation.

import numpy as np
import pandas as pd
from collections import defaultdict, deque
from config import ROLLING_WINDOW_SIZE

class StatsEngine:
    """
    A class to maintain rolling windows of spread data for pairs of exchanges
    and compute Z-scores in real-time.
    """
    def __init__(self):
        # For each (pair_of_exchanges, trading_pair), store a rolling list of spreads
        self.spread_data = defaultdict(lambda: deque(maxlen=ROLLING_WINDOW_SIZE))

    def calculate_spread(self, price_a, price_b):
        """
        Spread = price_a - price_b
        """
        if price_a is None or price_b is None:
            return None
        return price_a - price_b

    def update_spread_and_get_zscore(self, ex_a, ex_b, pair, spread):
        """
        Update rolling spread data for the given (ex_a, ex_b, pair),
        compute and return the Z-score for the new spread value.
        """
        key = (ex_a, ex_b, pair)
        if spread is not None:
            self.spread_data[key].append(spread)

        # Compute Z-score if we have enough data
        window_data = list(self.spread_data[key])
        if len(window_data) < 2:
            return None  # not enough data to compute std

        series = pd.Series(window_data)
        mean_ = series.mean()
        std_ = series.std()

        if std_ == 0 or np.isnan(std_):
            return None

        current_spread = window_data[-1]
        z_score = (current_spread - mean_) / std_
        return z_score

