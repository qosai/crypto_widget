COINS_FILE = "coins.txt"

def get_coins():
    """Load coins from file."""
    try:
        with open(COINS_FILE, "r") as file:
            return [line.strip().upper() for line in file.readlines()]
    except FileNotFoundError:
        return ["BTC", "ETH", "ADA", "BNB"]

def save_coins(coins):
    """Save the list of coins to a file."""
    with open(COINS_FILE, "w") as file:
        file.write("\n".join(coins))

def add_coin(coin, gui):
    """Add a coin and update UI."""
    coins = get_coins()
    if coin and coin not in coins and len(coin) <= 5:
        coins.append(coin)
        save_coins(coins)
        gui.refresh_dropdown()

def remove_coin(coin, gui):
    """Remove a coin and update UI."""
    coins = get_coins()
    if coin in coins:
        coins.remove(coin)
        save_coins(coins)
        gui.refresh_dropdown()
