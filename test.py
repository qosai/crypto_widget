from binance.client import Client

binance_client = Client()  # Ensure API keys are configured if needed

try:
    response = binance_client.ping()
    print("Binance API is reachable ✅")
except Exception as e:
    print(f"❌ Binance API is unreachable: {e}")

try:
    price = binance_client.get_symbol_ticker(symbol="BTCUSDT")
    print(f"BTC Price: {price}")
except Exception as e:
    print(f"❌ Error fetching BTC price: {e}")