import requests
import tkinter as tk
from tkinter import Label, OptionMenu, StringVar, Button, Entry, messagebox
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image
import pystray

# API Configuration
API_KEY = "c6b93fad-8f03-44cd-b02a-23c3d38db254"
LISTINGS_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
HISTORICAL_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical"

# Headers
HEADERS = {
    "X-CMC_PRO_API_KEY": API_KEY,
    "Accepts": "application/json",
}

# Default settings
COINS = ["BTC", "ETH", "ADA", "BNB", "MSTR"]
FIAT_CURRENCIES = ["USD", "EUR", "GBP"]
selected_fiat = "USD"

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

def update_prices():
    """Updates prices in the widget."""
    prices = get_crypto_prices()
    
    for symbol, label in labels.items():
        price = prices.get(symbol, "N/A")
        label.config(text=f"{symbol}: {selected_fiat} {price:.2f}" if isinstance(price, float) else f"{symbol}: {price}")
    
    root.after(60000, update_prices)  # Refresh every 60 seconds

def fetch_historical_data(symbol):
    """Fetches historical price data for the last 7 days."""
    try:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=7)
        
        params = {
            "symbol": symbol,
            "convert": selected_fiat,
            "time_start": int(start_time.timestamp()),
            "time_end": int(end_time.timestamp())
        }
        
        response = requests.get(HISTORICAL_URL, headers=HEADERS, params=params)
        data = response.json()
        
        if "data" in data and symbol in data["data"]:
            timestamps = [datetime.utcfromtimestamp(d["timestamp"]) for d in data["data"][symbol]]
            prices = [d["quote"][selected_fiat]["price"] for d in data["data"][symbol]]
            return timestamps, prices
        else:
            return [], []
    
    except Exception as e:
        return [], []

def show_price_chart():
    """Displays a historical price chart for the selected cryptocurrency."""
    symbol = selected_var.get()
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
        labels[coin] = Label(frame, text=f"{coin}: Loading...", font=("Arial", 14), fg="white", bg="#1E1E1E")
        labels[coin].pack(pady=2)

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
root.geometry("350x450")
root.configure(bg="#1E1E1E")

# Dropdown to select coin
selected_var = StringVar(root)
selected_var.set(COINS[0])  # Default selection
dropdown = OptionMenu(root, selected_var, *COINS)
dropdown.config(font=("Arial", 12), bg="white")
dropdown.pack(pady=10)

# Dropdown to select fiat currency
fiat_var = StringVar(root)
fiat_var.set(FIAT_CURRENCIES[0])  # Default selection
fiat_dropdown = OptionMenu(root, fiat_var, *FIAT_CURRENCIES, command=lambda _: update_prices())
fiat_dropdown.config(font=("Arial", 12), bg="white")
fiat_dropdown.pack(pady=5)

# Buttons to Add/Remove Cryptos
coin_entry = Entry(root, font=("Arial", 12))
coin_entry.pack(pady=5)

add_button = Button(root, text="Add Coin", command=add_coin, font=("Arial", 12), bg="green", fg="white")
add_button.pack(pady=5)

remove_button = Button(root, text="Remove Selected Coin", command=remove_coin, font=("Arial", 12), bg="red", fg="white")
remove_button.pack(pady=5)

# Button to show historical price chart
chart_button = Button(root, text="Show Price Chart", command=show_price_chart, font=("Arial", 12), bg="blue", fg="white")
chart_button.pack(pady=5)

# Minimize to tray button
tray_button = Button(root, text="Minimize to Tray", command=toggle_tray, font=("Arial", 12), bg="gray", fg="white")
tray_button.pack(pady=5)

# Frame for displaying coin prices
frame = tk.Frame(root, bg="#1E1E1E")
frame.pack(pady=10)

create_coin_labels()
update_prices()  # Initial price update

root.mainloop()