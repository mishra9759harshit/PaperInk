import os
import sys
import ctypes
import logging
import importlib
from engine import engine
from splash import PaperInkSplash
from gui import PaperInkDashboard
from tray import PaperInkTray
import database
from toolbar import Toolbar

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_admin():
    """Check if PaperInk is running with Administrator privileges (required for Magnification API)"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def relaunch_as_admin():
    """Relaunch the current script with elevated privileges using ShellExecuteW"""
    logging.info("Main: Requesting UAC elevation...")
    # Parameters: hwnd, lpOperation, lpFile, lpParameters, lpDirectory, nShowCmd
    res = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    if res > 32:
        sys.exit(0)
    else:
        logging.error(f"Main: UAC Elevation failed with error code: {res}")

class PaperInkApp:
    """Orchestrates the cinematic boot and high-performance E-Ink simulation"""

    def __init__(self):
        self.dashboard = None
        self.tray = None

        # Check Elevation First
        if not is_admin():
            relaunch_as_admin()
            return

        # 1. Initialize Database First
        database.init_db()

        # 2. Initialize Single Root window (hidden)
        self.dashboard = PaperInkDashboard(engine)
        self.dashboard.withdraw()
        self.dashboard.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        # Initialize Toolbar
        self.toolbar = Toolbar(self.dashboard)

        # 3. Check if first boot
        config_path = os.path.join(os.getenv("APPDATA"), "PaperInk", "config.json")
        is_first_boot = not os.path.exists(config_path)

        if is_first_boot:
            from first_boot import FirstBootSetup
            self.setup = FirstBootSetup(self.dashboard, on_complete=self.launch_splash)
        else:
            self.dashboard.after(100, self.launch_splash)

        # 4. Start Central Mainloop
        self.dashboard.mainloop()

    def launch_splash(self):
        splash_video = os.path.join(os.path.dirname(__file__), "assets", "boot_animation.mp4")
        self.splash = PaperInkSplash(self.dashboard, splash_video, on_complete=self.start_dashboard)

    def start_dashboard(self):
        """Transition completes, reveal dashboard and tray"""
        logging.info("Main: Transitioning to Dashboard")
        
        # Initialize Tray (Background persistence)
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.png")
        self.tray = PaperInkTray(
            icon_path=icon_path,
            on_show_dashboard=self.show_window,
            on_toggle_filter=self.toggle_engine,
            on_exit=self.cleanup
        )
        self.tray.start()
        
        # Start Heartbeat
        self.start_heartbeat()
        
        # Reveal UI
        self.dashboard.deiconify()
        if self.dashboard.overlay_enabled.get():
            self.toolbar.deiconify()

    def start_heartbeat(self):
        """Record one minute of usage every 60 seconds"""
        database.add_usage_minute()
        if self.dashboard:
            self.dashboard.after(60000, self.start_heartbeat)

    def show_window(self):
        """Restore the configuration dashboard from the tray"""
        if self.dashboard:
            self.dashboard.deiconify()
            self.dashboard.focus_force()

    def hide_window(self):
        """Minimize to system tray instead of exiting"""
        if self.dashboard:
            self.dashboard.withdraw()

    def toggle_engine(self):
        """Quick toggle for the E-Ink simulation via the tray icon"""
        if self.dashboard:
            new_state = not self.dashboard.filter_enabled.get()
            self.dashboard.filter_enabled.set(new_state)
            self.dashboard.save_config()

    def cleanup(self):
        """Safe shutdown of magnification engine and UI resources"""
        logging.info("Main: Cleaning up resources...")
        engine.stop()
        if self.dashboard:
            self.dashboard.quit()
        sys.exit(0)

if __name__ == "__main__":
    app = PaperInkApp()
