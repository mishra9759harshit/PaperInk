import pystray
from PIL import Image
import threading
import logging
import os

class PaperInkTray:
    """System Tray Integration for PaperInk v1.0"""

    def __init__(self, icon_path, on_show_dashboard, on_toggle_filter, on_exit):
        self.on_show_dashboard = on_show_dashboard
        self.on_toggle_filter = on_toggle_filter
        self.on_exit = on_exit

        # Load Icon
        try:
            image = Image.open(icon_path)
        except Exception as e:
            logging.error(f"Tray: Failed to load icon from {icon_path}: {e}")
            image = Image.new('RGB', (64, 64), color='gray') # Fallback

        # Menu Configuration
        menu = pystray.Menu(
            pystray.MenuItem("Configure PaperInk", self._show),
            pystray.MenuItem("Toggle E-Ink Mode", self._toggle),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self._exit)
        )

        self.icon = pystray.Icon("PaperInk", image, "PaperInk Display Pro", menu)
        self._thread = threading.Thread(target=self.icon.run, daemon=True)

    def _show(self, icon, item):
        if self.on_show_dashboard:
            self.on_show_dashboard()

    def _toggle(self, icon, item):
        if self.on_toggle_filter:
            self.on_toggle_filter()

    def _exit(self, icon, item):
        # Stop the tray icon
        self.icon.stop()
        if self.on_exit:
            self.on_exit()

    def start(self):
        """Starts the tray icon in a dedicated background thread"""
        self._thread.start()
        logging.info("PaperInk Tray: Thread started")

if __name__ == "__main__":
    tray = PaperInkTray("assets/icon.png", lambda: print("Show"), lambda: print("Toggle"), lambda: print("Exit"))
    tray.start()
    # Keep main thread alive for test
    import time
    while True: time.sleep(1)
