import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os
import database
from tree_canvas import BanyanTreeCanvas

class BanyanTreeHero(ctk.CTkFrame):
    """The Hero section displaying the dynamic Banyan Tree."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")
        
        self.title_label = ctk.CTkLabel(self, text="Focus Journey", font=ctk.CTkFont(size=24, weight="bold"), text_color="#2D2820")
        self.title_label.pack(pady=(10, 20))
        
        self.tree_canvas = BanyanTreeCanvas(self, width=250, height=250, bg="#FDFCF0")
        self.tree_canvas.pack(expand=True, fill=tk.BOTH)
        
        self.load_tree_state()
        
    def load_tree_state(self):
        tasks = database.get_daily_tasks()
        completed = sum(1 for t in tasks if t['completed'])
        pomodoro_mins = database.get_daily_pomodoro_minutes()
        usage_mins = database.get_total_usage_minutes()

        # Weighted score for growth
        growth_score = (completed * 10) + (pomodoro_mins) + (usage_mins // 5)
        self.tree_canvas.draw_tree(growth_score)

class PomodoroCard(ctk.CTkFrame):
    """Cinematic Card for Pomodoro Timer."""
    def __init__(self, master, on_update_tree=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Premium cinematic dark style for this card
        self.configure(fg_color="#1F1D1B", corner_radius=15, border_width=1, border_color="#3E3A33")
        self.on_update_tree = on_update_tree
        
        self.time_left = 25 * 60
        self.is_running = False
        self._timer_job = None

        self.setup_ui()

    def setup_ui(self):
        header = ctk.CTkLabel(self, text="POMODORO", font=ctk.CTkFont(size=14, weight="bold"), text_color="#A89F91")
        header.pack(pady=(15, 0))

        self.timer_label = ctk.CTkLabel(self, text="25:00", font=ctk.CTkFont(size=54, weight="bold"), text_color="#E8E3DB")
        self.timer_label.pack(pady=10)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))

        self.btn_start = ctk.CTkButton(btn_frame, text="▶", width=40, font=ctk.CTkFont(size=16), command=self.start_timer, fg_color="#FBC02D", text_color="#1F1D1B", hover_color="#F57F17")
        self.btn_start.pack(side=tk.LEFT, padx=5)
        self.btn_pause = ctk.CTkButton(btn_frame, text="⏸", width=40, font=ctk.CTkFont(size=16), command=self.pause_timer, fg_color="#3E3A33", hover_color="#5A5343")
        self.btn_pause.pack(side=tk.LEFT, padx=5)
        self.btn_reset = ctk.CTkButton(btn_frame, text="⟲", width=40, font=ctk.CTkFont(size=16), command=self.reset_timer, fg_color="#3E3A33", hover_color="#5A5343")
        self.btn_reset.pack(side=tk.LEFT, padx=5)

    def update_clock(self):
        mins, secs = divmod(self.time_left, 60)
        self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")
        if self.time_left > 0:
            self.time_left -= 1
            self._timer_job = self.after(1000, self.update_clock)
        else:
            self.is_running = False
            database.add_pomodoro_session(25)
            if self.on_update_tree:
                self.on_update_tree()
            self.reset_timer()

    def start_timer(self):
        if not self.is_running and self.time_left > 0:
            self.is_running = True
            self.update_clock()

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            if self._timer_job:
                self.after_cancel(self._timer_job)

    def reset_timer(self):
        self.pause_timer()
        self.time_left = 25 * 60
        mins, secs = divmod(self.time_left, 60)
        self.timer_label.configure(text=f"{mins:02d}:{secs:02d}")

class TasksCard(ctk.CTkFrame):
    """Cinematic Card for Focus Tasks."""
    def __init__(self, master, on_update_tree=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.configure(fg_color="#FFFFFF", corner_radius=15, border_width=1, border_color="#E0D8C8")
        self.on_update_tree = on_update_tree

        header = ctk.CTkLabel(self, text="TODAY'S MISSIONS", font=ctk.CTkFont(size=14, weight="bold"), text_color="#5A5343")
        header.pack(pady=(15, 10))

        self.task_list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.task_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        add_frame = ctk.CTkFrame(self, fg_color="transparent")
        add_frame.pack(fill=tk.X, padx=15, pady=15)

        self.task_entry = ctk.CTkEntry(add_frame, placeholder_text="Add task...", fg_color="#F8F6F0", text_color="#2D2820", border_width=0)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        btn_add = ctk.CTkButton(add_frame, text="+", width=30, height=30, command=self.add_task, fg_color="#5A5343", hover_color="#2D2820")
        btn_add.pack(side=tk.RIGHT)

        self.load_tasks()

    def load_tasks(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        tasks = database.get_daily_tasks()
        for t in tasks:
            var = tk.BooleanVar(value=t['completed'])
            cb = ctk.CTkCheckBox(self.task_list_frame, text=t['description'], variable=var, 
                                 command=lambda tid=t['id'], v=var: self.toggle_task(tid, v),
                                 text_color="#2D2820", fg_color="#5A5343", font=ctk.CTkFont(size=14))
            cb.pack(anchor="w", pady=6)

    def add_task(self):
        desc = self.task_entry.get()
        if desc.strip():
            database.add_task(desc)
            self.task_entry.delete(0, tk.END)
            self.load_tasks()
            if self.on_update_tree:
                self.on_update_tree()

    def toggle_task(self, task_id, var):
        database.update_task_status(task_id, var.get())
        if self.on_update_tree:
            self.on_update_tree()
