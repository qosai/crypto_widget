import requests
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, OptionMenu, StringVar, Frame, PhotoImage
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from binance.client import Client

import os
# Get the directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load icons AFTER initializing Tkinter (Use full paths)
up_icon = tk.PhotoImage(file=os.path.join(BASE_DIR, "up_arrow.png"))
down_icon = tk.PhotoImage(file=os.path.join(BASE_DIR, "down_arrow.png"))
chart_icon = tk.PhotoImage(file=os.path.join(BASE_DIR, "chart_icon.png"))



# API Configuration
API_KEY = "c6b93fad-8f03-44cd-b02a-23c3d38db254"
LISTINGS_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
COINS_FILE = "coins.txt"

# Headers
HEADERS = {
    "X-CMC_PRO_API_KEY": API_KEY,
    "Accepts": "application/json",
}

# Default settings
FIAT_CURRENCY = "USD"
binance_client = Client()
price_history = {}

# Load coins from text file
def load_coins():
    if os.path.exists(COINS_FILE):
        with open(COINS_FILE, "r") as file:
            return [line.strip().upper() for line in file.readlines()]
    return ["BTC", "ETH", "ADA", "BNB"]

# Save coins to text file
def save_coins():
    with open(COINS_FILE, "w") as file:
        file.write("\n".join(COINS))

COINS = load_coins()

def get_crypto_prices():
    """Fetches the latest cryptocurrency prices."""
    try:
        response = requests.get(LISTINGS_URL, headers=HEADERS, params={"convert": FIAT_CURRENCY})
        data = response.json()

        prices = {}
        for crypto in data["data"]:
            if crypto["symbol"] in COINS:
                prices[crypto["symbol"]] = crypto["quote"][FIAT_CURRENCY]["price"]

        return prices
    except Exception as e:
        return {}

def get_price_from_binance(symbol):
    """Fetches historical price data from Binance API for the last 10 minutes."""
    try:
        binance_symbol = f"{symbol}USDT"
        klines = binance_client.get_klines(symbol=binance_symbol, interval=Client.KLINE_INTERVAL_5MINUTE, limit=3)

        if len(klines) > 1:
            return float(klines[-2][4])  # Closing price from ~10 minutes ago
        return None
    except Exception as e:
        print(f"Error fetching Binance data: {e}")
        return None

def fetch_historical_data(symbol):
    """Fetches historical price data for the last 7 days."""
    try:
        binance_symbol = f"{symbol}USDT"
        klines = binance_client.get_klines(symbol=binance_symbol, interval=Client.KLINE_INTERVAL_1DAY, limit=7)

        timestamps = [datetime.fromtimestamp(k[0] / 1000) for k in klines]
        prices = [float(k[4]) for k in klines]  # Closing price

        return timestamps, prices
    except Exception as e:
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
    plt.ylabel(f"Price ({FIAT_CURRENCY})")
    plt.title(f"{symbol} Price Chart (Last 7 Days)")
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    plt.grid()

    plt.show()

def update_prices():
    """Updates prices in the widget and adds up/down indicators."""
    prices = get_crypto_prices()
    
    for symbol, frame in labels.items():
        current_price = prices.get(symbol, "N/A")

        if isinstance(current_price, float):
            formatted_price = f"{current_price:,.2f}"  # Add commas to format price
            old_price = get_price_from_binance(symbol)

            if old_price:
                price_diff = current_price - old_price
                if price_diff > 0:
                    indicator_icon = up_icon
                    color = "green"
                else:
                    indicator_icon = down_icon
                    color = "red"
            else:
                indicator_icon = None
                color = "white"

            # Update UI elements
            label, indicator_label, chart_button = frame
            label.config(text=f"{symbol}: {FIAT_CURRENCY} {formatted_price}", fg=color)
            if indicator_icon:
                indicator_label.config(image=indicator_icon)
                indicator_label.image = indicator_icon
            chart_button.config(command=lambda sym=symbol: show_price_chart(sym))
        else:
            labels[symbol][0].config(text=f"{symbol}: {current_price}", fg="white")

    root.after(600000, update_prices)  # Refresh every 10 minutes

def add_coin():
    """Adds a new cryptocurrency to the list and saves it."""
    global coin_dropdown

    new_coin = coin_entry.get().upper()

    if len(new_coin) > 5:
        messagebox.showwarning("Warning", "Coin symbol must be 5 characters or less!")
        return

    if new_coin in COINS:
        messagebox.showwarning("Warning", f"{new_coin} is already in the list!")
        return

    COINS.append(new_coin)
    save_coins()
    create_coin_labels()
    update_prices()
    refresh_dropdown()

def remove_coin():
    """Removes the selected cryptocurrency and updates storage."""
    global selected_var, coin_dropdown

    selected_coin = selected_var.get()

    if selected_coin in COINS:
        COINS.remove(selected_coin)
        save_coins()
        create_coin_labels()
        update_prices()
        refresh_dropdown()

def create_coin_labels():
    """Refreshes labels dynamically."""
    for widget in price_frame.winfo_children():
        widget.destroy()

    global labels
    labels = {}

    for coin in COINS:
        row = Frame(price_frame, bg="#1E1E1E")
        row.pack(pady=2, fill=tk.X)

        label = Label(row, text=f"{coin}: Loading...", font=("Arial", 14), fg="white", bg="#1E1E1E")
        label.pack(side=tk.LEFT, padx=5)

        indicator_label = Label(row, bg="#1E1E1E")
        indicator_label.pack(side=tk.LEFT, padx=5)

        chart_button = Button(row, image=chart_icon, bg="gray", command=lambda sym=coin: show_price_chart(sym))
        chart_button.pack(side=tk.RIGHT, padx=5)

        labels[coin] = (label, indicator_label, chart_button)

def refresh_dropdown():
    """Updates the dropdown menu dynamically when coins are added or removed."""
    global selected_var, coin_dropdown

    coin_dropdown.destroy()
    
    selected_var = StringVar(root)
    selected_var.set(COINS[0] if COINS else "")

    coin_dropdown = OptionMenu(remove_frame, selected_var, *COINS)
    coin_dropdown.pack(side=tk.LEFT, padx=5)

# Initialize Tkinter Window
root = tk.Tk()
root.title("Crypto Price Widget")
root.geometry("400x550")
root.configure(bg="#1E1E1E")

# Load icons AFTER initializing Tkinter (✅ FIXED)
up_icon = PhotoImage(file="up_arrow.png")
down_icon = PhotoImage(file="down_arrow.png")
chart_icon = PhotoImage(file="chart_icon.png")

# Prices Display Section
price_frame = Frame(root, bg="#1E1E1E")
price_frame.pack(pady=10)
create_coin_labels()
update_prices()

# Add Coin Section
coin_entry = Entry(root, font=("Arial", 12), width=6)
coin_entry.pack(pady=5)

add_button = Button(root, text="Add", command=add_coin, font=("Arial", 12), bg="green", fg="white")
add_button.pack(pady=5)

# Remove Coin Section
remove_frame = Frame(root, bg="#1E1E1E")
remove_frame.pack(pady=5)

selected_var = StringVar(root)
selected_var.set(COINS[0])

coin_dropdown = OptionMenu(remove_frame, selected_var, *COINS)
coin_dropdown.pack(side=tk.LEFT, padx=5)

remove_button = Button(remove_frame, text="Remove", command=remove_coin, font=("Arial", 12), bg="red", fg="white")
remove_button.pack(side=tk.LEFT)

root.mainloop()
