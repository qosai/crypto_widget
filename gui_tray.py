import threading
from pystray import Icon, MenuItem as item
from PIL import Image

class TrayManager:
    def __init__(self, app_instance, icon_path):
        self.app = app_instance
        self.icon = None
        self.icon_path = icon_path
        self.setup_tray_icon()

    def setup_tray_icon(self):
        """Initialize system tray icon and menu"""
        image = Image.open(self.icon_path)
        menu = (
            item("Show", self.restore_from_tray),
            item("Exit", self.app.exit_app)
        )
        self.icon = Icon("CryptoWidget", image, "Crypto Widget", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()

    def restore_from_tray(self, *args):
        """Restore main window from tray"""
        self.icon.visible = False
        self.app.root.deiconify()

    def stop(self):
        """Stop the tray icon"""
        if self.icon:
            self.icon.stop()