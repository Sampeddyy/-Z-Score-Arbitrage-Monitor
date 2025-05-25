import time
import ccxt
import threading
from collections import defaultdict, deque
from config import TARGET_EXCHANGES, TARGET_PAIRS, ROLLING_WINDOW_SIZE

class ExchangeDataFeed:
    """
    A class that connects to multiple exchanges via ccxt (REST) to fetch mid-prices in real time,
    with extra debug prints for each fetch.
    """
    def __init__(self):
        self.exchanges = {}
        for ex_id in TARGET_EXCHANGES:
            try:
                exchange_class = getattr(ccxt, ex_id)
                self.exchanges[ex_id] = exchange_class({"enableRateLimit": True})
            except Exception as e:
                print(f"Error initializing exchange {ex_id}: {e}")
                self.exchanges[ex_id] = None

        # Price storage: { (exchange, pair): (bid, ask, timestamp) }
        self.prices = defaultdict(lambda: {"bid": None, "ask": None, "timestamp": None})

        self.running = False

    def fetch_and_update_prices(self):
        while self.running:
            for ex_id, exchange in self.exchanges.items():
                if exchange is None:
                    continue  # skip if exchange didn't init
                for pair in TARGET_PAIRS:
                    try:
                        ticker = exchange.fetch_ticker(pair)
                        best_bid = ticker['bid'] if ticker['bid'] else 0
                        best_ask = ticker['ask'] if ticker['ask'] else 0
                        self.prices[(ex_id, pair)] = {
                            "bid": best_bid,
                            "ask": best_ask,
                            "timestamp": time.time()
                        }
                        mid_price = (best_bid + best_ask) / 2.0 if best_bid and best_ask else 0
                        print(f"[DEBUG] Fetched {ex_id} {pair}: bid={best_bid}, ask={best_ask}, mid={mid_price}")
                    except Exception as e:
                        print(f"Error fetching price from {ex_id} for {pair}: {e}")
            time.sleep(1)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.fetch_and_update_prices)
        self.thread.start()

    def stop(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()

    def get_mid_price(self, ex_id, pair):
        data = self.prices.get((ex_id, pair), None)
        if data is None:
            return None
        bid = data["bid"]
        ask = data["ask"]
        if bid is None or ask is None:
            return None
        return (bid + ask) / 2.0
