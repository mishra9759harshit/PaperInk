import customtkinter as ctk
import tkinter as tk
from sticky_notes import StickyNoteManager
import os
from PIL import Image

class Toolbar(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.master_root = master
        
        # Managers
        self.sticky_manager = StickyNoteManager(master)
        
        self.title("PaperInk Toolbar")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color="#18181A")
        
        # Core positioning
        self.screen_width = self.winfo_screenwidth()
        self.collapsed_width = 80
        self.expanded_width = 750 # Expanded to fit new widgets
        self.height = 70
        self.y = 0
        
        self.collapse_geometry()
        self.attributes("-alpha", 0.5) 

        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

        self.tools_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon_draw.png")
        if os.path.exists(icon_path):
            img = Image.open(icon_path).resize((24, 24))
            self.trigger_icon = ctk.CTkImage(light_image=img, dark_image=img, size=(24, 24))
        else:
            self.trigger_icon = None

        self.trigger_lbl = ctk.CTkLabel(self, text="▼" if not self.trigger_icon else "", image=self.trigger_icon, text_color="white")
        self.trigger_lbl.pack(expand=True, fill=tk.BOTH)

        self.setup_tools()

    def collapse_geometry(self):
        x = (self.screen_width // 2) - (self.collapsed_width // 2)
        self.geometry(f"{self.collapsed_width}x30+{x}+{self.y}")

    def expand_geometry(self):
        x = (self.screen_width // 2) - (self.expanded_width // 2)
        self.geometry(f"{self.expanded_width}x{self.height}+{x}+{self.y}")

    def load_icon(self, name, size=(24, 24)):
        path = os.path.join(os.path.dirname(__file__), "assets", name)
        if os.path.exists(path):
            img = Image.open(path).resize(size)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        return None

    def setup_tools(self):
        icon_sticky = self.load_icon("icon_sticky.png")

        base_color = "#282A36"
        hover_color = "#44475A"

        # 1. Timer / Clock
        self.time_label = ctk.CTkLabel(self.tools_frame, text="00:00", font=ctk.CTkFont(size=20, weight="bold"), text_color="#F1FA8C", width=80)
        self.time_label.pack(side=tk.LEFT, padx=15)
        
        ctk.CTkLabel(self.tools_frame, text="|", text_color="#555").pack(side=tk.LEFT, padx=5)
        
        # 2. Open Dashboard Button
        dashboard_btn = ctk.CTkButton(self.tools_frame, text="Dashboard", width=90, height=35, command=self.open_dashboard, fg_color=base_color, hover_color=hover_color)
        dashboard_btn.pack(side=tk.LEFT, padx=10)

        # 3. Theme Dropdown
        themes = ["KindleClassic", "Paper ink", "SepiaManuscript", "HighContrastEInk", "SoftPaper", "SolarizedLight", "AgedPaper", "NeutralDark"]
        self.theme_opt = ctk.CTkOptionMenu(self.tools_frame, values=themes, variable=self.master_root.current_mode, command=self.change_theme, width=130, height=35, fg_color=base_color)
        self.theme_opt.pack(side=tk.LEFT, padx=10)

        # 4. Engine Toggle Switch
        self.filter_switch = ctk.CTkSwitch(self.tools_frame, text="E-Ink Filter", variable=self.master_root.filter_enabled, command=self.toggle_filter, progress_color="#50FA7B", text_color="white")
        self.filter_switch.pack(side=tk.LEFT, padx=10)
        
        ctk.CTkLabel(self.tools_frame, text="|", text_color="#555").pack(side=tk.LEFT, padx=5)

        # Misc (Sticky Notes)
        ctk.CTkButton(self.tools_frame, text="", image=icon_sticky, width=45, height=45, command=self.add_note, fg_color="#F1FA8C", hover_color="#FFF06B").pack(side=tk.LEFT, padx=10)

        # Start timer clock
        self.update_clock()

    def on_hover(self, event):
        self.attributes("-alpha", 1.0)
        self.trigger_lbl.pack_forget()
        self.expand_geometry()
        self.tools_frame.pack(expand=True, fill=tk.BOTH, pady=8)

    def on_leave(self, event):
        if event.y > self.height - 5 or event.x < 5 or event.x > self.expanded_width - 5:
            self.attributes("-alpha", 0.5)
            self.tools_frame.pack_forget()
            self.collapse_geometry()
            self.trigger_lbl.pack(expand=True, fill=tk.BOTH)

    def add_note(self):
        self.sticky_manager.new_note()

    def update_clock(self):
        import time
        if hasattr(self.master_root, 'pomodoro_card') and self.master_root.pomodoro_card.is_running:
            mins, secs = divmod(self.master_root.pomodoro_card.time_left, 60)
            self.time_label.configure(text=f"🍅 {mins:02d}:{secs:02d}")
        else:
            self.time_label.configure(text=time.strftime("%H:%M"))
        
        self.after(1000, self.update_clock)

    def open_dashboard(self):
        if self.master_root.state() == "withdrawn" or self.master_root.state() == "iconic":
            self.master_root.deiconify()
        self.master_root.focus_force()

    def change_theme(self, choice):
        self.master_root.save_config()

    def toggle_filter(self, *args):
        self.master_root.save_config()
