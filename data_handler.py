import requests
import tkinter as tk
from datetime import datetime
from binance.client import Client
from coin_manager import get_coins

# Binance Client Configuration
binance_client = Client()

# Binance allowed intervals (Match exactly with dropdown values)
BINANCE_INTERVAL_MAP = {
    "5 Minutes": Client.KLINE_INTERVAL_5MINUTE,
    "15 Minutes": Client.KLINE_INTERVAL_15MINUTE,
    "1 Hour": Client.KLINE_INTERVAL_1HOUR,
    "1 Day": Client.KLINE_INTERVAL_1DAY
}

# API Configuration
API_KEY = "c6b93fad-8f03-44cd-b02a-23c3d38db254"
LISTINGS_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

def get_crypto_prices():
    """Fetch current cryptocurrency prices from CoinMarketCap API."""
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY,
    }
    params = {"convert": "USD"}  # Fetch prices in USD

    try:
        response = requests.get(LISTINGS_URL, headers=headers, params=params)
        data = response.json()
        
        if "data" not in data:
            print(f"⚠ API Error: {data}")
            return {}

        prices = {}
        for coin in data["data"]:
            symbol = coin["symbol"]
            if symbol in get_coins():
                prices[symbol] = float(coin["quote"]["USD"]["price"])

        return prices

    except Exception as e:
        print(f"⚠ Error fetching CoinMarketCap prices: {e}")
        return {}





def get_historical_price(symbol, interval):
    """Fetch historical price data from Binance API."""
    try:
        binance_symbol = f"{symbol}USDT"
        klines = binance_client.get_klines(
            symbol=binance_symbol,
            interval=interval,
            limit=2
        )
        return float(klines[0][4]) if len(klines) >= 2 else None
    except Exception as e:
        print(f"⚠ Error fetching historical data for {symbol}: {e}")
        return None


def update_prices(gui):
    """Update price labels and indicators in the GUI."""
    interval_key = gui.selected_interval.get()
    interval_value = BINANCE_INTERVAL_MAP.get(interval_key, Client.KLINE_INTERVAL_1HOUR)
    
    prices = get_crypto_prices()  # ✅ Fetch current prices from CoinMarketCap

    for symbol in get_coins():
        if symbol not in gui.ui.labels:
            continue
            
        label_widget = gui.ui.labels[symbol]
        current_price = prices.get(symbol)  # CoinMarketCap price
        old_price = get_historical_price(symbol, interval_value)  # Binance historical price

        # Update price display
        price_text = f"{symbol}: {current_price:,.2f} USD" if current_price else f"{symbol}: N/A"
        label_widget.config(text=price_text, fg="white")

        # Update price indicator (Green = Up, Red = Down)
        if current_price and old_price:
            price_diff = current_price - old_price
            indicator_icon = gui.up_icon if price_diff > 0 else gui.down_icon
            label_widget.config(image=indicator_icon, compound=tk.RIGHT)
            label_widget.image = indicator_icon

    # Schedule next update using Tkinter's built-in scheduler
    refresh_time = get_refresh_time(interval_key)
    gui.root.after(refresh_time, lambda: update_prices(gui))







def get_refresh_time(interval_str):
    """Convert interval string to milliseconds."""
    return {
        "5 Minutes": 300_000,    # 5 minutes
        "15 Minutes": 900_000,   # 15 minutes
        "1 Hour": 3_600_000,     # 1 hour
        "1 Day": 86_400_000      # 1 day
    }.get(interval_str, 3_600_000)  # Default to 1 hour

# ... (keep show_price_chart and fetch_historical_data functions unchanged)