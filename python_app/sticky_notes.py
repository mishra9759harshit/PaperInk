import customtkinter as ctk
import tkinter as tk
import uuid
import database

class StickyNote(ctk.CTkToplevel):
    def __init__(self, master=None, note_id=None, content="", x=100, y=100, color="#FFEB3B"):
        super().__init__(master)
        
        self.note_id = note_id or str(uuid.uuid4())
        self.color = color
        
        self.title("Sticky Note")
        self.geometry(f"200x200+{x}+{y}")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color=self.color)
        
        # Header for dragging
        self.header = ctk.CTkFrame(self, height=20, corner_radius=0, fg_color="#FBC02D")
        self.header.pack(fill=tk.X, side=tk.TOP)
        self.header.bind("<Button-1>", self.start_drag)
        self.header.bind("<B1-Motion>", self.do_drag)
        self.header.bind("<ButtonRelease-1>", self.save_state)

        # Close button
        self.close_btn = ctk.CTkButton(self.header, text="X", width=20, height=20, 
                                       fg_color="transparent", text_color="black", hover_color="#F57F17",
                                       command=self.delete_note)
        self.close_btn.pack(side=tk.RIGHT)

        # Text Area
        self.textbox = ctk.CTkTextbox(self, fg_color=self.color, text_color="black", wrap="word", corner_radius=0)
        self.textbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.textbox.insert("1.0", content)
        self.textbox.bind("<KeyRelease>", self.schedule_save)
        
        self._save_job = None

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def do_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def schedule_save(self, event=None):
        if self._save_job:
            self.after_cancel(self._save_job)
        self._save_job = self.after(1000, self.save_state)

    def save_state(self, event=None):
        content = self.textbox.get("1.0", "end-1c")
        x = self.winfo_x()
        y = self.winfo_y()
        database.save_sticky_note(self.note_id, content, x, y, self.color)

    def delete_note(self):
        database.delete_sticky_note(self.note_id)
        self.destroy()

class StickyNoteManager:
    def __init__(self, master_root):
        self.master_root = master_root
        self.notes = []

    def load_all(self):
        saved = database.get_sticky_notes()
        for note in saved:
            n = StickyNote(self.master_root, note['id'], note['content'], note['x'], note['y'], note['color'])
            self.notes.append(n)

    def new_note(self):
        n = StickyNote(self.master_root)
        n.save_state()
        self.notes.append(n)
