import requests
import tkinter as tk
from tkinter import Label

# API Configuration
API_KEY = "c6b93fad-8f03-44cd-b02a-23c3d38db254"
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# Headers
HEADERS = {
    "X-CMC_PRO_API_KEY": API_KEY,
    "Accepts": "application/json",
}

# List of cryptocurrencies to display
COINS = ["BTC", "ETH", "ADA", "BNB"]

def get_crypto_prices():
    """Fetches the latest cryptocurrency prices."""
    try:
        response = requests.get(URL, headers=HEADERS, params={"convert": "USD"})
        data = response.json()

        prices = {}
        for crypto in data["data"]:
            if crypto["symbol"] in COINS:
                prices[crypto["symbol"]] = crypto["quote"]["USD"]["price"]

        return prices
    except Exception as e:
        return {"Error": str(e)}

def update_prices():
    """Updates prices in the widget."""
    prices = get_crypto_prices()
    
    for symbol, label in labels.items():
        price = prices.get(symbol, "N/A")
        label.config(text=f"{symbol}: ${price:.2f}" if isinstance(price, float) else f"{symbol}: {price}")
    
    root.after(60000, update_prices)  # Refresh every 60 seconds

# Create Widget using Tkinter
root = tk.Tk()
root.title("Crypto Price Widget")
root.geometry("300x200")

# Create labels for each coin
labels = {}
for i, coin in enumerate(COINS):
    labels[coin] = Label(root, text=f"{coin}: Loading...", font=("Arial", 14))
    labels[coin].pack()

update_prices()  # Initial price update

root.mainloop()