import tkinter as tk
from tkinter import Label, Frame, Button, Entry, OptionMenu, StringVar
from coin_manager import add_coin as cm_add_coin, remove_coin as cm_remove_coin, get_coins

class UIComponents:
    def __init__(self, root, app_instance):
        self.root = root
        self.app = app_instance
        self.labels = {}

    def setup_tray(self):
        """Setup the system tray icon."""
        icon_path = self.get_icon_path("tray_icon.ico")  # Ensure this file exists
        self.tray = TrayManager(self, icon_path)

    def create_price_list(self, coins, chart_icon):
        """Create dynamic list of coins with prices"""
        if hasattr(self, 'price_frame'):
            self.price_frame.destroy()
        
        self.price_frame = Frame(self.root, bg="#1E1E1E")
        self.price_frame.pack(pady=10, fill=tk.X)
        self.labels = {}

        for coin in coins:
            row = Frame(self.price_frame, bg="#1E1E1E")
            row.pack(pady=2, fill=tk.X)

            lbl = Label(row, text=f"{coin}: Loading...", 
                        font=("Arial", 14), fg="white", bg="#1E1E1E")
            lbl.pack(side=tk.LEFT, padx=5)

            chart_btn = Button(row, image=chart_icon, bg="gray", 
                               command=lambda s=coin: self.app.show_price_chart(s))
            chart_btn.image = chart_icon
            chart_btn.pack(side=tk.RIGHT, padx=5)

            self.labels[coin] = lbl

    def create_interval_section(self, intervals, current_interval):
        """Create interval selection components"""
        interval_frame = Frame(self.root, bg="#1E1E1E")
        interval_frame.pack(pady=5)
        Label(interval_frame, text="Interval:", bg="#1E1E1E", fg="white").pack(side=tk.LEFT)
        OptionMenu(interval_frame, self.app.selected_interval, *intervals.keys(),
                   command=self.app.change_interval).pack(side=tk.LEFT)

    def create_coin_management(self):
        """Create add/remove coin components"""
        # Add Coin Section
        add_frame = Frame(self.root, bg="#1E1E1E")
        add_frame.pack(pady=5)
        self.coin_entry = Entry(add_frame, width=8, font=("Arial", 12))
        self.coin_entry.pack(side=tk.LEFT)
        Button(add_frame, text="Add", command=self.add_coin, 
               bg="green", fg="white").pack(side=tk.LEFT)

        # Remove Coin Section
        remove_frame = Frame(self.root, bg="#1E1E1E")
        remove_frame.pack(pady=5)
        self.coin_dropdown = OptionMenu(remove_frame, self.app.selected_coin, *get_coins())
        self.coin_dropdown.pack(side=tk.LEFT)
        Button(remove_frame, text="Remove", command=self.remove_coin, 
               bg="red", fg="white").pack(side=tk.LEFT)

    def add_coin(self):
        """Add a new coin and update UI"""
        coin = self.coin_entry.get().strip().upper()
        if coin:
            cm_add_coin(coin, self)
            self.refresh_dropdown()

    def remove_coin(self):
        """Remove a coin and update UI"""
        coin = self.app.selected_coin.get()
        if coin:
            cm_remove_coin(coin, self)
            self.refresh_dropdown()

    def refresh_dropdown(self):
        """Refresh the dropdown options after adding/removing coins"""
        menu = self.coin_dropdown["menu"]
        menu.delete(0, "end")
        for coin in get_coins():
            menu.add_command(label=coin, command=lambda value=coin: self.app.selected_coin.set(value))
