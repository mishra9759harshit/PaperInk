import customtkinter as ctk
import tkinter as tk
import time

class FirstBootSetup(ctk.CTkToplevel):
    def __init__(self, master, on_complete):
        super().__init__(master)
        self.on_complete = on_complete
        
        self.title("PaperInk - Setup")
        self.geometry("600x400")
        self.overrideredirect(True) # Borderless
        self.configure(fg_color="#FDFCF0")
        
        # Center Window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.attributes("-topmost", True)

        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = ctk.CTkLabel(self, text="PaperInk Setup", font=ctk.CTkFont(size=32, weight="bold", family="Georgia"), text_color="#2D2820")
        header.pack(pady=(50, 10))
        
        sub = ctk.CTkLabel(self, text="Preparing your cinematic productivity environment.", font=ctk.CTkFont(size=14), text_color="#5A5343")
        sub.pack(pady=(0, 30))

        # Warning
        warning_frame = ctk.CTkFrame(self, fg_color="#FEEBC8", corner_radius=10, border_width=1, border_color="#F6AD55")
        warning_frame.pack(padx=50, fill=tk.X, pady=(0, 30))
        
        warn_lbl = ctk.CTkLabel(warning_frame, text="Please be patient. First time setup may take 1-2 minutes.", font=ctk.CTkFont(size=13, weight="bold"), text_color="#C05621")
        warn_lbl.pack(pady=15, padx=15)

        # Progress Section
        self.status_label = ctk.CTkLabel(self, text="Initializing...", font=ctk.CTkFont(size=14, weight="bold"), text_color="#2D2820")
        self.status_label.pack(pady=(20, 10))

        self.progressbar = ctk.CTkProgressBar(self, width=400, height=15, progress_color="#5A5343", fg_color="#E0D8C8")
        self.progressbar.pack(pady=10)
        self.progressbar.set(0)

        # Start sequence
        self.tasks = [
            ("Checking Windows Architecture...", 0.1),
            ("Allocating Local Database Space...", 0.3),
            ("Generating Cinematic Color Matrices...", 0.5),
            ("Configuring Application Dependencies...", 0.7),
            ("Resolving Startup Configurations...", 0.85),
            ("Optimizing Environment...", 0.95),
            ("Finishing Setup...", 1.0)
        ]
        self.task_idx = 0
        
        self.after(1000, self.process_next_task)

    def process_next_task(self):
        if self.task_idx < len(self.tasks):
            desc, progress = self.tasks[self.task_idx]
            self.status_label.configure(text=desc)
            self.progressbar.set(progress)
            self.task_idx += 1
            
            # Artificial delay to mimic a robust setup process (1-2 minutes requested)
            # For demonstration, we'll use 3-4 seconds per task to equate to ~25 seconds total
            # in a real setup, it could be longer
            self.after(3500, self.process_next_task)
        else:
            self.after(1000, self.finish)

    def finish(self):
        self.destroy()
        self.on_complete()

# For testing
if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    app = FirstBootSetup(root, lambda: print("Done"))
    root.mainloop()
