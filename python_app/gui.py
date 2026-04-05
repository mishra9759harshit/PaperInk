import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os
import json
import webbrowser
from engine import PaperInkEngine
from pomodoro import BanyanTreeHero, PomodoroCard, TasksCard

# Configure Appearance
ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue") 

class PaperInkDashboard(ctk.CTk):
    """Modern Configuration Dashboard with Cinematic Layout"""

    def __init__(self, engine: PaperInkEngine, parent_app=None):
        super().__init__()
        self.engine = engine
        self.parent_app = parent_app
        
        # Window setup
        self.title("PaperInk Dashboard")
        self.geometry("1100x750")
        self.configure(fg_color="#FDFCF0") # Warm paper background
        
        # Internal State
        self.config_path = os.path.join(os.getenv("APPDATA"), "PaperInk", "config.json")
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        self.load_config()

        # Layout (3 Columns)
        self.grid_columnconfigure(0, weight=0, minsize=260) # Settings
        self.grid_columnconfigure(1, weight=1)              # Hero (Tree)
        self.grid_columnconfigure(2, weight=0, minsize=350) # Productivity Cards
        self.grid_rowconfigure(0, weight=1)

        # UI Components
        self.setup_sidebar()
        self.setup_hero()
        self.setup_productivity_cards()
        
        # Sync Initial State
        self.engine.set_filter(
            theme_name=self.current_mode.get(),
            intensity=self.intensity_slider.get(),
            enabled=self.filter_enabled.get()
        )

    def load_config(self):
        defaults = {"mode": "KindleClassic", "intensity": 0.8, "enabled": False, "overlay_enabled": True}
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    self.config_data = {**defaults, **json.load(f)}
            except:
                self.config_data = defaults
        else:
            self.config_data = defaults

        self.current_mode = tk.StringVar(value=self.config_data["mode"])
        self.filter_enabled = tk.BooleanVar(value=self.config_data["enabled"])
        self.overlay_enabled = tk.BooleanVar(value=self.config_data["overlay_enabled"])

    def save_config(self):
        self.config_data = {
            "mode": self.current_mode.get(),
            "intensity": self.intensity_slider.get(),
            "enabled": self.filter_enabled.get(),
            "overlay_enabled": self.overlay_enabled.get()
        }
        with open(self.config_path, "w") as f:
            json.dump(self.config_data, f)
        
        # Sync Engine
        self.engine.set_filter(
            theme_name=self.config_data["mode"],
            intensity=self.config_data["intensity"],
            enabled=self.config_data["enabled"]
        )
        
        # Sync Toolbar Overlay
        if self.parent_app and hasattr(self.parent_app, "toolbar"):
            if self.overlay_enabled.get():
                self.parent_app.toolbar.deiconify()
            else:
                self.parent_app.toolbar.withdraw()

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, corner_radius=0, fg_color="#F0E6D2")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="PaperInk", font=ctk.CTkFont(size=28, weight="bold", family="Georgia"), text_color="#2D2820")
        self.logo_label.pack(pady=(30, 5), padx=20, anchor="w")
        
        self.v_label = ctk.CTkLabel(self.sidebar, text="Cinematic Edition", font=ctk.CTkFont(size=12), text_color="#5A5343")
        self.v_label.pack(pady=0, padx=20, anchor="w")

        # Overlay Toggle
        overlay_frame = ctk.CTkFrame(self.sidebar, fg_color="#FFFFFF", corner_radius=10)
        overlay_frame.pack(fill=tk.X, padx=20, pady=(30, 20))
        ctk.CTkLabel(overlay_frame, text="Tools Overlay", font=ctk.CTkFont(weight="bold"), text_color="#2D2820").pack(side=tk.LEFT, padx=15, pady=15)
        ctk.CTkSwitch(overlay_frame, text="", variable=self.overlay_enabled, command=self.save_config, progress_color="#F57F17").pack(side=tk.RIGHT, padx=15)

        # Filter Section
        ctk.CTkLabel(self.sidebar, text="DISPLAY FILTER", font=ctk.CTkFont(size=12, weight="bold"), text_color="#807662").pack(anchor="w", padx=20, pady=(20, 5))
        filter_frame = ctk.CTkFrame(self.sidebar, fg_color="#FFFFFF", corner_radius=10)
        filter_frame.pack(fill=tk.X, padx=20)
        ctk.CTkLabel(filter_frame, text="Enable Engine", text_color="#2D2820").pack(side=tk.LEFT, padx=15, pady=15)
        ctk.CTkSwitch(filter_frame, text="", variable=self.filter_enabled, command=self.save_config, progress_color="#5A5343").pack(side=tk.RIGHT, padx=15)

        # Themes
        ctk.CTkLabel(self.sidebar, text="Themes", font=ctk.CTkFont(weight="bold"), text_color="#5A5343").pack(anchor="w", padx=20, pady=(20, 10))
        themes = ["KindleClassic", "Paper ink", "SepiaManuscript", "HighContrastEInk", "SoftPaper", "SolarizedLight", "AgedPaper", "NeutralDark"]
        for theme in themes:
            btn = ctk.CTkRadioButton(self.sidebar, text=theme, variable=self.current_mode, value=theme, command=self.save_config, text_color="#5A5343", border_color="#5A5343", hover_color="#D4C9B0")
            btn.pack(anchor="w", padx=25, pady=5)

        # Intensity
        ctk.CTkLabel(self.sidebar, text="Intensity", font=ctk.CTkFont(weight="bold"), text_color="#5A5343").pack(anchor="w", padx=20, pady=(20, 10))
        self.intensity_slider = ctk.CTkSlider(self.sidebar, from_=0, to=1, command=lambda x: self.save_config(), button_color="#5A5343", progress_color="#5A5343")
        self.intensity_slider.set(self.config_data["intensity"])
        self.intensity_slider.pack(fill=tk.X, padx=20)

        # Sidebar Footer (Links & Copyright)
        footer_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        # Social Icons
        social_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        social_frame.pack(pady=(0, 10))

        # Helper for icons in footer
        github_icon = self.load_footer_icon("icon_github.png")
        coffee_icon = self.load_footer_icon("icon_coffee.png")

        if github_icon:
            gh_btn = ctk.CTkButton(social_frame, text="", image=github_icon, width=30, height=30, fg_color="transparent", hover_color="#D4C9B0", command=lambda: webbrowser.open("https://github.com/mishra9759harshit"))
            gh_btn.pack(side=tk.LEFT, padx=10)

        if coffee_icon:
            cf_btn = ctk.CTkButton(social_frame, text="", image=coffee_icon, width=30, height=30, fg_color="transparent", hover_color="#D4C9B0", command=lambda: webbrowser.open("https://www.buymeacoffee.com/"))
            cf_btn.pack(side=tk.LEFT, padx=10)

        ctk.CTkLabel(footer_frame, text="© BitRo Lab's", font=ctk.CTkFont(size=12), text_color="#807662").pack()

    def load_footer_icon(self, name):
        # We find assets relative to this file
        path = os.path.join(os.path.dirname(__file__), "assets", name)
        if os.path.exists(path):
            img = Image.open(path)
            return ctk.CTkImage(light_image=img, dark_image=img, size=(24, 24))
        return None

    def setup_hero(self):
        self.hero_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.hero_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.hero_frame.grid_columnconfigure(0, weight=1)
        self.hero_frame.grid_rowconfigure(0, weight=1)
        
        self.banyan_tree = BanyanTreeHero(self.hero_frame)
        self.banyan_tree.grid(row=0, column=0, sticky="nsew")

    def setup_productivity_cards(self):
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=0, column=2, sticky="nsew", padx=(0, 20), pady=30)
        
        # Function to pass to cards so they can tell the tree to update
        update_tree_cb = self.banyan_tree.load_tree_state
        
        self.pomodoro_card = PomodoroCard(self.cards_frame, on_update_tree=update_tree_cb)
        self.pomodoro_card.pack(fill=tk.X, pady=(0, 20))
        
        self.tasks_card = TasksCard(self.cards_frame, on_update_tree=update_tree_cb)
        self.tasks_card.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    from engine import engine
    app = PaperInkDashboard(engine)
    app.mainloop()
