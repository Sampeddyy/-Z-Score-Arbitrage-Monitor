# 📈 Z-Score Arbitrage Monitor

A modular Python-based bot that monitors Z-score deviations between asset pairs across exchanges to identify arbitrage opportunities in real-time. Built for traders, quants, and crypto automation enthusiasts.

![Python](https://img.shields.io/badge/built_with-python-blue?logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## 🔍 Overview

Z-Score Arbitrage is a statistical trading strategy that detects divergence from mean price relationships between two correlated assets. This bot automatically:

- Fetches live market data from multiple exchanges
- Calculates Z-score over a rolling window
- Triggers alerts when thresholds are breached
- Logs actionable trade signals

---

## ⚙️ Features

- 📊 Real-time price tracking from APIs
- 📐 Rolling Z-score computation with configurable window
- 🔔 Signal alerts via console/log
- 🧱 Modular components for:
  - Signal management
  - Statistical engine
  - Data streaming
  - Alert routing

---

## 🧩 Folder Structure
| File / Folder       | Description                               |
|---------------------|-------------------------------------------|
| `main.py`           | Entry point of the bot                    |
| `config.py`         | Global thresholds and strategy settings   |
| `data_feed.py`      | Market data ingestion from exchanges      |
| `stats_engine.py`   | Z-score calculator logic                  |
| `signal_manager.py` | Signal generation based on thresholds     |
| `alert_system.py`   | Alerts/notifications when signals fire    |
| `storage.py`        | Local storage for historical price data   |
| `requirements.txt`  | Python package dependencies               |


## 💡 Usage

```bash
pip install -r requirements.txt
python main.py
Tech Stack
Python 3.x

Numpy / Pandas

REST APIs (for live price feeds)

Modular OOP architecture

🛡️ License
This project is licensed under the MIT License.
See the LICENSE file for details.
