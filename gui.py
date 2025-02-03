import tkinter as tk
import sys
import os
from tkinter import PhotoImage
from coin_manager import get_coins
from data_handler import BINANCE_INTERVAL_MAP
from gui_tray import TrayManager
from gui_components import UIComponents

class CryptoGUI:

    def setup_tray(self):
        """Setup the system tray icon."""
        icon_path = self.get_icon_path("tray_icon.ico")  # Ensure this file exists
        self.tray = TrayManager(self, icon_path)

    def get_icon_path(self, filename):
        """إرجاع المسار الكامل للملفات داخل مجلد الأيقونات."""
        return os.path.join(os.path.dirname(__file__), "icons", filename)



    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Crypto Price Widget")
        self.root.geometry("400x600")
        self.root.configure(bg="#1E1E1E")
        self.root.overrideredirect(True)
        
        # Initialize core components
        self.selected_interval = tk.StringVar(value="1 Hour")
        self.selected_coin = tk.StringVar()
        self.ui = UIComponents(self.root, self)
        self.tray = None
        
        # Setup application
        self.setup_window()
        self.load_assets()
        self.create_close_button()
        self.setup_ui_components()
        self.setup_tray()
        self.update_prices()

    def start_move(self, event):
        """تسجيل إحداثيات بداية السحب."""
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        """تحريك النافذة عند سحبها."""
        dx = event.x - self.x
        dy = event.y - self.y
        self.root.geometry(f"+{self.root.winfo_x() + dx}+{self.root.winfo_y() + dy}")

    def stop_move(self, event):
        """إيقاف السحب."""
        self.x = None
        self.y = None

    def setup_window(self):
        """Configure main window properties"""
        self.root.iconbitmap(self.get_icon_path("chart_icon.ico"))
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.on_move)

    def load_assets(self):
        """Load images and icons"""
        self.chart_icon = PhotoImage(file=self.get_icon_path("chart_icon.png"))
        self.up_icon = PhotoImage(file=self.get_icon_path("up_arrow.png"))
        self.down_icon = PhotoImage(file=self.get_icon_path("down_arrow.png"))

    def setup_ui_components(self):
        """Initialize all UI components"""
        self.ui.create_price_list(get_coins(), self.chart_icon)
        self.ui.create_interval_section(BINANCE_INTERVAL_MAP, self.selected_interval)
        self.ui.create_coin_management()

    # ... (keep other methods like start_move, do_move, etc)

    def update_prices(self):
        """Trigger price updates with current interval"""
        interval = BINANCE_INTERVAL_MAP[self.selected_interval.get()]
        # Call your data_handler.update_prices with the interval
        # Example: update_prices(interval, self.update_ui)

    def refresh_ui(self):
        """Refresh all dynamic UI elements"""
        self.ui.create_price_list(get_coins(), self.chart_icon)
        self.update_dropdown_options()

    def exit_app(self):
        """Clean exit procedure"""
        self.tray.stop()
        self.root.quit()
        self.root.destroy()
    
    def create_close_button(self):
        """إنشاء زر إغلاق النافذة"""
        close_btn = tk.Button(self.root, text="X", command=self.exit_app, bg="red", fg="white", font=("Arial", 12), bd=0, relief=tk.FLAT)
        close_btn.place(x=370, y=10, width=20, height=20)

    def change_interval(self, selected_interval):
        """تحديث الفاصل الزمني بناءً على اختيار المستخدم."""
        self.selected_interval.set(selected_interval)
        self.update_prices()  # إعادة تحديث الأسعار بناءً على الفاصل الزمني الجديد


    def run(self):
        self.root.mainloop()

def get_icon_path(filename):
    """Resolve path for assets"""
    base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
    return os.path.join(base_path, "assets", filename)