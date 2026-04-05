import tkinter as tk
import math
import random

class BanyanTreeCanvas(tk.Canvas):
    def __init__(self, master, **kwargs):
        # Default to a nice paper-like background if not provided
        kwargs.setdefault("bg", "#FDFCF0")
        kwargs.setdefault("highlightthickness", 0)
        super().__init__(master, **kwargs)
        
    def draw_tree(self, growth_score):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1: # Window not yet rendered fully
            self.after(100, lambda: self.draw_tree(growth_score))
            return

        # Base parameters
        trunk_x = width // 2
        trunk_y = height - 20
        
        # Scaling factors based on growth_score (min 1, max 100 for complexity)
        # growth_score could be (completed_tasks * 10 + pomodoro_minutes + total_usage // 10)
        max_depth = min(4 + (growth_score // 20), 10)
        branch_len = 50 + (growth_score // 5)
        
        # Draw Main Trunk
        self.branch(trunk_x, trunk_y, -90, max_depth, branch_len, stroke_width=max_depth*2)
        
        # Draw Aerial Roots for Banyan effect (if growth is sufficient)
        if growth_score > 50:
            num_roots = min((growth_score - 50) // 20, 5)
            for i in range(num_roots):
                rx = trunk_x + random.randint(-100, 100)
                ry = trunk_y - random.randint(50, 150)
                self.create_line(rx, ry, rx, height - 10, fill="#5A5343", width=2, dash=(4, 4))

    def branch(self, x, y, angle, depth, length, stroke_width):
        if depth == 0:
            self.draw_leaf(x, y)
            return

        # Calculate end point
        nx = x + length * math.cos(math.radians(angle))
        ny = y + length * math.sin(math.radians(angle))
        
        # Draw branch
        color = "#2D2820" if depth > 2 else "#5A5343"
        self.create_line(x, y, nx, ny, fill=color, width=stroke_width, capstyle=tk.ROUND)
        
        # Recursive calls
        new_length = length * 0.75
        new_width = max(stroke_width * 0.7, 1)
        
        # Banyan trees often have multiple "sub-trunks"
        spread = 25 + random.randint(-5, 5)
        self.branch(nx, ny, angle - spread, depth - 1, new_length, new_width)
        self.branch(nx, ny, angle + spread, depth - 1, new_length, new_width)
        
        # Extra branch for density at higher levels
        if depth > 4 and random.random() > 0.6:
            self.branch(nx, ny, angle + random.randint(-10, 10), depth - 1, new_length * 0.8, new_width)

    def draw_leaf(self, x, y):
        # "Nano banana" leaf: elongated oval
        leaf_color = random.choice(["#43A047", "#2E7D32", "#66BB6A"])
        # Rotate slightly
        angle = random.randint(0, 360)
        r = 6
        lx = x + r * math.cos(math.radians(angle))
        ly = y + r * math.sin(math.radians(angle))
        
        # Draw small elongated oval
        self.create_oval(x-2, y-5, x+2, y+5, fill=leaf_color, outline="")
        
        # Optional "fruit" (tiny yellow dot)
        if random.random() > 0.9:
            self.create_oval(x-1, y-1, x+1, y+1, fill="#FBC02D", outline="")
