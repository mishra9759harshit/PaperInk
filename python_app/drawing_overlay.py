import tkinter as tk
from drawing_engine import DrawingEngine

class DrawingOverlay(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("PaperInk Drawing Overlay")
        self.attributes("-fullscreen", True)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.4)
        self.config(bg="#FDFCF0")
        self.overrideredirect(True)

        self.canvas = tk.Canvas(self, bg="#FDFCF0", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.engine = DrawingEngine()

        # Drawing State
        self.current_tool = "pen"  # "pen", "highlighter", "eraser", "rect", "line", "circle"
        self.color = "#E53935"
        self.line_width = 3
        self.last_x, self.last_y = None, None
        
        self.temp_id = None # for shape previews
        
        self.setup_bindings()

    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def set_tool(self, tool="pen"):
        self.current_tool = tool
        if tool == "highlighter":
            # Don't overwrite color if user already picked one, but default to yellow for highlighter if it's the first time
            if self.color == "#E53935": # default red
                self.color = "#FFEB3B" 
            self.line_width = 15
        elif tool == "eraser":
            self.color = "#FDFCF0" 
            self.line_width = 30
        elif tool == "pen":
            self.line_width = 3

    def set_color(self, color):
        if self.current_tool not in ["eraser"]:
            self.color = color

    def set_size(self, size):
        self.line_width = float(size)

    def perform_action(self, action):
        if action == "undo":
            if self.engine.undo():
                self.redraw()
        elif action == "redo":
            if self.engine.redo():
                self.redraw()
        elif action == "clear":
            self.clear()

    def redraw(self):
        self.canvas.delete("all")
        for stroke in self.engine.get_all_strokes():
            coords = stroke["coords"]
            kwargs = stroke["kwargs"]
            t = stroke["type"]
            
            if t in ["pen", "highlighter", "eraser"]:
                if len(coords) >= 4:
                    self.canvas.create_line(*coords, **kwargs)
            elif t == "rect":
                self.canvas.create_rectangle(*coords, outline=kwargs["fill"], width=kwargs["width"])
            elif t == "line":
                self.canvas.create_line(*coords, fill=kwargs["fill"], width=kwargs["width"])
            elif t == "circle":
                self.canvas.create_oval(*coords, outline=kwargs["fill"], width=kwargs["width"])

    def on_press(self, event):
        self.last_x, self.last_y = event.x, event.y
        
        kwargs = {"fill": self.color, "width": self.line_width, "capstyle": tk.ROUND, "smooth": True}
        if self.current_tool == "highlighter":
            kwargs["stipple"] = "gray50"
            
        self.engine.begin_stroke(self.current_tool, **kwargs)
        self.engine.add_point(self.last_x, self.last_y)

        if self.current_tool in ["rect", "line", "circle"]:
            if self.current_tool == "rect":
                self.temp_id = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline=self.color, width=self.line_width)
            elif self.current_tool == "line":
                self.temp_id = self.canvas.create_line(event.x, event.y, event.x, event.y, fill=self.color, width=self.line_width)
            elif self.current_tool == "circle":
                self.temp_id = self.canvas.create_oval(event.x, event.y, event.x, event.y, outline=self.color, width=self.line_width)

    def on_drag(self, event):
        if not self.engine.current_stroke: return
        
        kwargs = self.engine.current_stroke["kwargs"]
        
        if self.current_tool in ["pen", "highlighter", "eraser"]:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, **kwargs)
            self.engine.add_point(event.x, event.y)
            self.last_x, self.last_y = event.x, event.y
            
        elif self.current_tool in ["rect", "line", "circle"] and self.temp_id:
            start_x, start_y = self.engine.current_stroke["coords"][0], self.engine.current_stroke["coords"][1]
            self.canvas.coords(self.temp_id, start_x, start_y, event.x, event.y)

    def on_release(self, event):
        if not self.engine.current_stroke: return
        
        if self.current_tool in ["rect", "line", "circle"]:
            start_x, start_y = self.engine.current_stroke["coords"][0], self.engine.current_stroke["coords"][1]
            # Finalize coords for the engine
            self.engine.current_stroke["coords"] = [start_x, start_y, event.x, event.y]
        
        self.engine.commit_stroke()
        self.temp_id = None
        self.last_x, self.last_y = None, None

    def clear(self):
        self.engine.clear_all()
        self.canvas.delete("all")
