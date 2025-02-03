import requests
import tkinter as tk
from tkinter import Label, OptionMenu, StringVar, Button, Entry, messagebox
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from io import BytesIO
from PIL import Image
import pystray
from binance.client import Client

# API Configuration
API_KEY = "c6b93fad-8f03-44cd-b02a-23c3d38db254"
LISTINGS_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# Headers
HEADERS = {
    "X-CMC_PRO_API_KEY": API_KEY,
    "Accepts": "application/json",
}

# Default settings
COINS = ["BTC", "ETH", "ADA", "BNB", "MSTR"]
FIAT_CURRENCIES = ["USD", "EUR", "GBP"]
selected_fiat = "USD"

# Binance API (No API key required for public market data)
binance_client = Client()

def get_crypto_prices():
    """Fetches the latest cryptocurrency prices."""
    try:
        response = requests.get(LISTINGS_URL, headers=HEADERS, params={"convert": selected_fiat})
        data = response.json()

        prices = {}
        for crypto in data["data"]:
            if crypto["symbol"] in COINS:
                prices[crypto["symbol"]] = crypto["quote"][selected_fiat]["price"]

        return prices
    except Exception as e:
        return {"Error": str(e)}

def get_price_one_hour_ago(symbol):
    """Fetches price from 1 hour ago using Binance API."""
    try:
        binance_symbol = f"{symbol}USDT"
        klines = binance_client.get_klines(symbol=binance_symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=2)
        if len(klines) > 1:
            return float(klines[0][4])  # Closing price 1 hour ago
        return None
    except Exception as e:
        print(f"Error fetching historical price: {e}")
        return None

def fetch_historical_data(symbol):
    """Fetches historical price data for the last 7 days from Binance."""
    try:
        binance_symbol = f"{symbol}USDT"
        klines = binance_client.get_klines(symbol=binance_symbol, interval=Client.KLINE_INTERVAL_1DAY, limit=7)

        timestamps = [datetime.fromtimestamp(k[0] / 1000) for k in klines]
        prices = [float(k[4]) for k in klines]  # Closing price

        return timestamps, prices
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return [], []

def show_price_chart(symbol):
    """Displays a historical price chart when clicking on a cryptocurrency."""
    timestamps, prices = fetch_historical_data(symbol)

    if not timestamps:
        messagebox.showerror("Error", "No historical data found!")
        return

    plt.figure(figsize=(6, 4))
    plt.plot(timestamps, prices, marker='o', linestyle='-', color='blue', label=f"{symbol} Price")

    plt.xlabel("Date")
    plt.ylabel(f"Price ({selected_fiat})")
    plt.title(f"{symbol} Price Chart (Last 7 Days)")
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    plt.grid()

    plt.show()

def update_prices():
    """Updates prices in the widget and adds up/down indicators."""
    prices = get_crypto_prices()
    
    for symbol, label in labels.items():
        current_price = prices.get(symbol, "N/A")

        if isinstance(current_price, float):
            formatted_price = f"{current_price:,.2f}"  # Add commas to format price
            old_price = get_price_one_hour_ago(symbol)
            if old_price:
                price_diff = current_price - old_price
                indicator = "📉⬇️" if price_diff < 0 else "📈⬆️"
                label.config(text=f"{symbol}: {selected_fiat} {formatted_price} {indicator}")
            else:
                label.config(text=f"{symbol}: {selected_fiat} {formatted_price} (No Data)")
        else:
            label.config(text=f"{symbol}: {current_price}")

    root.after(60000, update_prices)  # Refresh every 60 seconds

def add_coin():
    """Adds a new cryptocurrency to the list."""
    new_coin = coin_entry.get().upper()
    
    if new_coin in COINS:
        messagebox.showwarning("Warning", f"{new_coin} is already in the list!")
        return

    COINS.append(new_coin)
    create_coin_labels()
    update_prices()

def remove_coin():
    """Removes the selected cryptocurrency."""
    selected_coin = selected_var.get()
    
    if selected_coin in COINS:
        COINS.remove(selected_coin)
        create_coin_labels()
        update_prices()

def create_coin_labels():
    """Refreshes labels dynamically."""
    for widget in frame.winfo_children():
        widget.destroy()
    
    global labels
    labels = {}
    for coin in COINS:
        label = Label(frame, text=f"{coin}: Loading...", font=("Arial", 14), fg="white", bg="#1E1E1E", cursor="hand2")
        label.pack(pady=2)
        label.bind("<Button-1>", lambda e, symbol=coin: show_price_chart(symbol))  # Click to show chart
        labels[coin] = label

def toggle_tray():
    """Minimizes to system tray and creates an icon."""
    root.withdraw()

    def restore_window(icon, item):
        """Restores the application window from the tray."""
        icon.stop()
        root.deiconify()

    image = Image.new("RGB", (64, 64), (0, 0, 0))  # Creates a blank icon

    menu = pystray.MenuItem("Restore", restore_window)
    icon = pystray.Icon("CryptoWidget", image, menu=pystray.Menu(menu))
    icon.run()

# Create Widget using Tkinter
root = tk.Tk()
root.title("Crypto Price Widget")
root.geometry("350x500")
root.configure(bg="#1E1E1E")

# Frame for displaying coin prices
frame = tk.Frame(root, bg="#1E1E1E")
frame.pack(pady=10)

create_coin_labels()
update_prices()  # Initial price update

# Add / Remove Cryptocurrency Section (At Bottom)
coin_entry = Entry(root, font=("Arial", 12))
coin_entry.pack(pady=5)

add_button = Button(root, text="Add Coin", command=add_coin, font=("Arial", 12), bg="green", fg="white")
add_button.pack(pady=5)

remove_button = Button(root, text="Remove Selected Coin", command=remove_coin, font=("Arial", 12), bg="red", fg="white")
remove_button.pack(pady=5)

root.mainloop()