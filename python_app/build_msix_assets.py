import os
from PIL import Image

def create_msix_assets():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "assets", "icon.png")
    
    if not os.path.exists(icon_path):
        print(f"Error: {icon_path} not found.")
        return

    # Load Source Icon
    img = Image.open(icon_path).convert("RGBA")
    
    # Store the output in a dedicated MSStore_Assets folder
    out_dir = os.path.join(base_dir, "MSStore_Assets")
    os.makedirs(out_dir, exist_ok=True)

    # 1. StoreLogo (50x50)
    store_logo = img.resize((50, 50), Image.Resampling.LANCZOS)
    store_logo.save(os.path.join(out_dir, "StoreLogo.png"))

    # 2. Square150x150Logo
    sq150 = img.resize((150, 150), Image.Resampling.LANCZOS)
    sq150.save(os.path.join(out_dir, "Square150x150Logo.png"))

    # 3. Square44x44Logo
    sq44 = img.resize((44, 44), Image.Resampling.LANCZOS)
    sq44.save(os.path.join(out_dir, "Square44x44Logo.png"))

    # 4. Wide310x150Logo
    # Create transparent 310x150, paste 150x150 in center
    wide = Image.new("RGBA", (310, 150), (0, 0, 0, 0))
    # center is (310-150)//2 = 80
    wide.paste(sq150, (80, 0), mask=sq150)
    wide.save(os.path.join(out_dir, "Wide310x150Logo.png"))

    # 5. SplashScreen (620x300)
    # Create transparent 620x300, paste 300x300 in center
    splash = Image.new("RGBA", (620, 300), (0, 0, 0, 0))
    sq300 = img.resize((300, 300), Image.Resampling.LANCZOS)
    # center is (620-300)//2 = 160
    splash.paste(sq300, (160, 0), mask=sq300)
    splash.save(os.path.join(out_dir, "SplashScreen.png"))

    print("MSIX Assets successfully generated in MSStore_Assets/")

if __name__ == "__main__":
    create_msix_assets()
