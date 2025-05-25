import time
from data_feed import ExchangeDataFeed
from stats_engine import StatsEngine
from signal_manager import SignalManager
from alert_system import send_alerts
from storage import init_db, store_signal
from config import TARGET_PAIRS

def main():
    print("Starting Cross-Exchange Arbitrage Signal System...")

    # Initialize optional DB if desired
    db_conn = init_db()

    # Initialize data feed
    data_feed = ExchangeDataFeed()
    data_feed.start()

    # Initialize stats engine & signal manager
    stats_engine = StatsEngine()
    signal_manager = SignalManager()

    try:
        while True:
            # Build a list of valid exchanges (skip any that didn't init)
            ex_list = [
                ex_id for ex_id, ex_obj in data_feed.exchanges.items()
                if ex_obj is not None
            ]

            # Compare each pair of distinct exchanges
            for i in range(len(ex_list)):
                for j in range(i + 1, len(ex_list)):
                    ex_a = ex_list[i]
                    ex_b = ex_list[j]

                    # For each configured trading pair
                    for trading_pair in TARGET_PAIRS:
                        price_a = data_feed.get_mid_price(ex_a, trading_pair)
                        price_b = data_feed.get_mid_price(ex_b, trading_pair)
                        if price_a is None or price_b is None:
                            # Debug print: no valid price yet
                            print(f"[DEBUG] Skipping {trading_pair} for {ex_a} - {ex_b} (price None).")
                            continue

                        # Calculate spread
                        spread = stats_engine.calculate_spread(price_a, price_b)
                        # Update rolling & get z-score
                        
                        z_score = stats_engine.update_spread_and_get_zscore(
                            ex_a, ex_b, trading_pair, spread
                        )

                        # Print debug info
                        print(f"[DEBUG] Checking {ex_a} vs {ex_b}, pair={trading_pair}, "
                              f"priceA={price_a:.2f}, priceB={price_b:.2f}, "
                              f"spread={spread:.2f}, z_score={z_score}")

                        # Check if a signal is triggered
                        signal_data = signal_manager.check_signal(
                            ex_a=ex_a,
                            ex_b=ex_b,
                            pair=trading_pair,
                            z_score=z_score,
                            price_a=price_a,
                            price_b=price_b,
                            spread=spread
                        )

                        if signal_data is not None:
                            print("***** SIGNAL DETECTED *****")
                            print(signal_data)
                            # Send alerts
                            send_alerts(signal_data)
                            # Store signal in DB (optional)
                            store_signal(db_conn, signal_data)

            # Sleep a bit to avoid busy-waiting
            time.sleep(1)

    except KeyboardInterrupt:
        print("Shutting down arbitrage bot...")

    finally:
        # Clean shutdown
        data_feed.stop()
        if db_conn:
            db_conn.close()

if __name__ == "__main__":
    main()
