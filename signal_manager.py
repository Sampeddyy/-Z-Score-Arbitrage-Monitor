# signal_manager.py
# Applies the mean reversion logic and thresholds to generate signals.

import time
from config import (
    Z_SCORE_THRESHOLD,
    MIN_SPREAD_PCT,
    SIGNAL_COOLDOWN
)

class SignalManager:
    """
    Checks if conditions are met to trigger an arbitrage signal 
    (|Z-score| >= threshold and spread >= min percentage).
    Applies cooldown so the same pair/exchanges aren't spammed.
    """
    def __init__(self):
        # Record the last time we triggered a signal for a given key
        # key could be (ex_a, ex_b, pair, direction) or something simpler
        self.last_signal_time = {}

    def check_signal(
        self, 
        ex_a, 
        ex_b, 
        pair, 
        z_score, 
        price_a, 
        price_b, 
        spread
    ):
        """
        Returns a dict with signal info if triggered, else None.
        """
        if z_score is None:
            return None

        # Calculate min spread in raw price terms
        # e.g., if MIN_SPREAD_PCT=0.002, for price ~ $20,000, raw_spread_req=40
        avg_price = (price_a + price_b) / 2.0 if price_a and price_b else None
        if not avg_price:
            return None

        raw_spread_req = avg_price * MIN_SPREAD_PCT
        if abs(spread) < raw_spread_req:
            return None  # spread not large enough

        if abs(z_score) < Z_SCORE_THRESHOLD:
            return None  # not statistically significant

        # Determine direction
        if z_score > 0:
            # Price_A is higher than Price_B by a lot
            direction = "SELL A, BUY B"
        else:
            # Price_B is higher than Price_A by a lot
            direction = "BUY A, SELL B"

        # Cooldown check
        key = (ex_a, ex_b, pair, direction)
        current_time = time.time()
        if key not in self.last_signal_time:
            self.last_signal_time[key] = 0

        if (current_time - self.last_signal_time[key]) < SIGNAL_COOLDOWN:
            return None  # still in cooldown

        # Record the new trigger time
        self.last_signal_time[key] = current_time

        # Build the signal data
        signal_data = {
            "timestamp": current_time,
            "pair": pair,
            "exchange_a": ex_a,
            "price_a": price_a,
            "exchange_b": ex_b,
            "price_b": price_b,
            "spread": spread,
            "z_score": z_score,
            "direction": direction
        }
        return signal_data

