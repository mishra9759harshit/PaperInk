import ctypes
from ctypes import wintypes
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MAGCOLOREFFECT(ctypes.Structure):
    """Windows Magnification API Color Effect Matrix (5x5)"""
    _fields_ = [("transform", ctypes.c_float * 25)]

class PaperInkEngine:
    """Core E-Ink Simulation Engine using Windows Magnification API"""
    
    # High-Fidelity E-Ink Color Matrices (5x5)
    THEMES = {
        "KindleClassic": [
            0.299, 0.587, 0.114, 0.0, 0.0,  # Red row
            0.299, 0.587, 0.114, 0.0, 0.0,  # Green row
            0.299, 0.587, 0.114, 0.0, 0.0,  # Blue row
            0.0,   0.0,   0.0,   1.0, 0.0,  # Alpha row
            0.1,   0.1,   0.1,   0.0, 1.0   # Offset row (Warmth)
        ],
        "Paper ink": [
            0.33, 0.33, 0.33, 0.0, 0.0,
            0.33, 0.33, 0.33, 0.0, 0.0,
            0.33, 0.33, 0.33, 0.0, 0.0,
            0.0,  0.0,  0.0,  1.0, 0.0,
            0.0,  0.0,  0.0,  0.0, 1.0
        ],
        "SepiaManuscript": [
            0.393, 0.769, 0.189, 0.0, 0.0,
            0.349, 0.686, 0.168, 0.0, 0.0,
            0.272, 0.534, 0.131, 0.0, 0.0,
            0.0,   0.0,   0.0,   1.0, 0.0,
            0.05,  0.02,  0.0,   0.0, 1.0
        ],
        "HighContrastEInk": [
            0.5, 0.5, 0.5, 0.0, 0.0,
            0.5, 0.5, 0.5, 0.0, 0.0,
            0.5, 0.5, 0.5, 0.0, 0.0,
            0.0, 0.0, 0.0, 1.0, 0.0,
            -0.1, -0.1, -0.1, 0.0, 1.0
        ],
        "SoftPaper": [
            0.25, 0.50, 0.10, 0.0, 0.0,
            0.25, 0.50, 0.10, 0.0, 0.0,
            0.25, 0.50, 0.10, 0.0, 0.0,
            0.0,  0.0,  0.0,  1.0, 0.0,
            0.15, 0.15, 0.12, 0.0, 1.0
        ],
        "SolarizedLight": [
            0.992, 0.0,   0.0,   0.0, 0.0,
            0.0,   0.965, 0.0,   0.0, 0.0,
            0.0,   0.0,   0.890, 0.0, 0.0,
            0.0,   0.0,   0.0,   1.0, 0.0,
            0.0,   0.0,   0.0,   0.0, 1.0
        ],
        "AgedPaper": [
            0.960, 0.0,   0.0,   0.0, 0.0,
            0.0,   0.960, 0.0,   0.0, 0.0,
            0.0,   0.0,   0.862, 0.0, 0.0,
            0.0,   0.0,   0.0,   1.0, 0.0,
            0.0,   0.0,   0.0,   0.0, 1.0
        ],
        "NeutralDark": [
            -0.90,  0.0,   0.0,   0.0, 0.0,
             0.0,  -0.90,  0.0,   0.0, 0.0,
             0.0,   0.0,  -0.90,  0.0, 0.0,
             0.0,   0.0,   0.0,   1.0, 0.0,
             0.95,  0.95,  0.95,  0.0, 1.0
        ]
    }

    def __init__(self):
        self.mag = None
        try:
            self.mag = ctypes.WinDLL("Magnification.dll")
            self._initialized = self.mag.MagInitialize()
            logging.info("PaperInk Engine: Magnification API Initialized")
        except Exception as e:
            logging.error(f"PaperInk Engine: Failed to initialize Magnification API: {e}")
            self._initialized = False

    def set_filter(self, theme_name="KindleClassic", intensity=1.0, enabled=True):
        """Applies a global display filter based on theme and intensity"""
        if not self._initialized:
            return False

        if not enabled:
            # Identity Matrix (Resets filter)
            matrix = [
                1.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 1.0
            ]
        else:
            base_matrix = self.THEMES.get(theme_name, self.THEMES["KindleClassic"])
            # Blend with identity based on intensity if needed (simplified for now)
            matrix = base_matrix

        effect = MAGCOLOREFFECT()
        # Ensure matrix is exactly 25 floats
        effect.transform[:] = matrix

        try:
            res = self.mag.MagSetFullscreenColorEffect(ctypes.byref(effect))
            if res:
                logging.info(f"PaperInk Engine: Filter updated -> Theme: {theme_name}, Enabled: {enabled}")
            return res
        except Exception as e:
            logging.error(f"PaperInk Engine: Failed to set color effect: {e}")
            return False

    def stop(self):
        """Cleanup Magnification API resources"""
        if self._initialized and self.mag:
            # Reset to identity before quitting
            self.set_filter(enabled=False)
            self.mag.MagUninitialize()
            logging.info("PaperInk Engine: API Uninitialized")

# Singleton instance
engine = PaperInkEngine()
