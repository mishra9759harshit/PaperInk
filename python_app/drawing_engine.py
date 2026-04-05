class DrawingEngine:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []
        
        # A stroke is a dictionary: {"type": "path", "coords": [...], "kwargs": {}}
        self.current_stroke = None

    def begin_stroke(self, stroke_type, **kwargs):
        self.current_stroke = {"type": stroke_type, "coords": [], "kwargs": kwargs}

    def add_point(self, x, y):
        if self.current_stroke:
            self.current_stroke["coords"].extend([x, y])

    def commit_stroke(self):
        if self.current_stroke and len(self.current_stroke["coords"]) > 2:
            self.undo_stack.append(self.current_stroke)
            self.redo_stack.clear() # clear redo history on new action
        self.current_stroke = None

    def undo(self):
        if self.undo_stack:
            stroke = self.undo_stack.pop()
            self.redo_stack.append(stroke)
            return True
        return False

    def redo(self):
        if self.redo_stack:
            stroke = self.redo_stack.pop()
            self.undo_stack.append(stroke)
            return True
        return False

    def clear_all(self):
        self.undo_stack.clear()
        self.redo_stack.clear()

    def get_all_strokes(self):
        return self.undo_stack
