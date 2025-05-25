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
Z-Score Arbitrage Monitor/
├── main.py             # Entry point
├── config.py           # Global thresholds and settings
├── data_feed.py        # Market data ingestion
├── stats_engine.py     # Z-score calculator
├── signal_manager.py   # Signal generation logic
├── alert_system.py     # Triggers/alerts
├── storage.py          # Optional local storage for price logs
├── requirements.txt    # Python dependencies

---

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
