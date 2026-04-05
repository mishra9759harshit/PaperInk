import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import logging
import time

class PaperInkSplash:
    """Cinematic Boot Experience for PaperInk v1.0 using OpenCV for stability"""

    def __init__(self, master, video_path, on_complete):
        self.root = tk.Toplevel(master)
        self.on_complete = on_complete
        self.video_path = video_path
        
        # Window Setup
        self.root.title("PaperInk Booting")
        self.root.geometry("800x450")
        self.root.overrideredirect(True)  # Borderless cinematic
        self.root.configure(bg="black")
        
        # Center on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - 400
        y = (screen_height // 2) - 225
        self.root.geometry(f"800x450+{x}+{y}")

        # Canvas for video
        self.canvas = tk.Canvas(self.root, width=800, height=450, bg="black", highlightthickness=0)
        self.canvas.pack()

        # Initialize OpenCV capture
        if os.path.exists(video_path):
            self.cap = cv2.VideoCapture(video_path)
            
            # Try to determine total frames for smooth progress calculation
            self.total_frames = 150 # Fallback
            try:
                frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                if frames > 0:
                    self.total_frames = frames
            except:
                pass
                
            self.current_frame = 0
            self._play_video()
        else:
            logging.error(f"Splash: Video not found at {video_path}")
            self.root.after(1000, self._finish)

    def _play_video(self):
        """Processes and displays video frames using OpenCV and Tkinter"""
        ret, frame = self.cap.read()
        if ret:
            self.current_frame += 1
            progress = min(self.current_frame / self.total_frames, 1.0)
            
            # Formulate text based on progress
            if progress < 0.3:
                task_text = "Task: Initializing Fast Boot Subsystems..."
            elif progress < 0.6:
                task_text = "Task: Loading PaperInk Database..."
            elif progress < 0.9:
                task_text = "Task: Restoring Workspace Context..."
            else:
                task_text = "Task: Launching Cinematic Dashboard..."

            # Resize frame to fit canvas
            frame = cv2.resize(frame, (800, 450))
            
            # Add Cinematic Overlays directly onto frame before converting to RGB
            font = cv2.FONT_HERSHEY_SIMPLEX
            # Drop shadow for text readability
            cv2.putText(frame, task_text, (20, 420), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, task_text, (20, 420), font, 0.5, (230, 230, 230), 1, cv2.LINE_AA)
            
            # Progress Bar Track (Background)
            cv2.rectangle(frame, (20, 435), (780, 440), (40, 40, 40), -1)
            # Progress Bar Fill (Warm color matching theme)
            bar_width = int(20 + (760 * progress))
            cv2.rectangle(frame, (20, 435), (bar_width, 440), (220, 190, 160), -1)

            # Convert OpenCV BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Create PhotoImage
            self.img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
            
            # Schedule next frame (approx 33ms for 30fps)
            self.root.after(30, self._play_video)
        else:
            # Video ended
            self.cap.release()
            self._finish()

    def _finish(self):
        """Transition from Splash to Dashboard"""
        self.root.destroy()
        if self.on_complete:
            self.on_complete()

# For testing
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    splash = PaperInkSplash(root, "assets/boot_animation.mp4", lambda: root.destroy())
    root.mainloop()
