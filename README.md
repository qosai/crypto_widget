# crypto_widget
Desktop widget to fetch crypto prices

# 🪙 Crypto Price Widget

A **Windows 11 widget** built with Python that **displays real-time cryptocurrency prices**, shows **historical price charts**, and triggers **price alerts when a coin moves ±5% in 10 minutes**. It fetches data from **CoinMarketCap & Binance APIs** and supports **persistent coin selection**.

---

## ✨ Features
✅ **Real-time crypto prices** (updated every 10 minutes)  
✅ **Price alerts 🚨** (triggers if price moves ±5% in 10 minutes)  
✅ **Click on a price to view the historical chart 📈**  
✅ **Up/down indicators 📉⬇️ / 📈⬆️** based on last price  
✅ **Persistent coin list (saved in `coins.txt`)**  
✅ **Easily add/remove coins dynamically**  
✅ **Formatted price with thousands separator (`42,350.25`)**  

---

## 📂 Project Structure
CryptoWidget/
│── crypto_widget.py      # Main script
│── requirements.txt      # Dependencies for the project
│── coins.txt             # Stores the list of selected cryptocurrencies
│── README.md             # Project documentation


## 🛠️ Installation

1️⃣ **Clone the Repository**
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/CryptoWidget.git
cd CryptoWidget

2️⃣ Create a Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Widget
python crypto_widget.py

