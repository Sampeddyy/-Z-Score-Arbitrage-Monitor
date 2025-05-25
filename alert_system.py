# alert_system.py
# Implements various alert delivery methods (email, Telegram, Discord).

import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import (
    ALERT_EMAIL_ENABLED,
    ALERT_TELEGRAM_ENABLED,
    ALERT_DISCORD_ENABLED,
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_SENDER,
    EMAIL_PASSWORD,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    DISCORD_WEBHOOK_URL
)

def send_email_alert(subject, body, to_email):
    """Send an email alert using SMTP."""
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        print("Email alert sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_telegram_alert(message):
    """Send a Telegram message using the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            print("Telegram alert sent successfully!")
        else:
            print(f"Error sending Telegram alert: {resp.text}")
    except Exception as e:
        print(f"Telegram exception: {e}")

def send_discord_alert(message):
    """Send a message to a Discord channel via webhook."""
    payload = {"content": message}
    try:
        resp = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        if resp.status_code == 204 or resp.status_code == 200:
            print("Discord alert sent successfully!")
        else:
            print(f"Error sending Discord alert: {resp.text}")
    except Exception as e:
        print(f"Discord exception: {e}")

def send_alerts(signal_data, to_email="recipient@example.com"):
    """
    Takes signal_data dict, composes an alert message, 
    sends via configured channels.
    """
    timestamp = signal_data["timestamp"]
    pair = signal_data["pair"]
    ex_a = signal_data["exchange_a"]
    p_a = signal_data["price_a"]
    ex_b = signal_data["exchange_b"]
    p_b = signal_data["price_b"]
    spread = signal_data["spread"]
    z_score = signal_data["z_score"]
    direction = signal_data["direction"]

    alert_msg = (
        f"Arbitrage Signal Detected!\n"
        f"Timestamp: {timestamp}\n"
        f"Pair: {pair}\n"
        f"{ex_a} Price: {p_a}\n"
        f"{ex_b} Price: {p_b}\n"
        f"Spread: {spread}\n"
        f"Z-Score: {z_score}\n"
        f"Direction: {direction}\n"
    )

    # Send email
    if ALERT_EMAIL_ENABLED:
        send_email_alert(f"Arbitrage Signal: {pair}", alert_msg, to_email)

    # Send Telegram
    if ALERT_TELEGRAM_ENABLED:
        send_telegram_alert(alert_msg)

    # Send Discord
    if ALERT_DISCORD_ENABLED:
        send_discord_alert(alert_msg)

