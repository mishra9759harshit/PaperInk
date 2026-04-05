import os
from PIL import Image

def generate_assets(source_path, output_dir):
    if not os.path.exists(source_path):
        print(f"Error: Source {source_path} not found.")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    img = Image.open(source_path)
    
    # MSIX Required Sizes
    assets = {
        "StoreLogo.png": (50, 50),
        "Square150x150Logo.png": (150, 150),
        "Square44x44Logo.png": (44, 44),
        "Wide310x150Logo.png": (310, 150),
        "SplashScreen.png": (620, 300)
    }
    
    for filename, size in assets.items():
        # Handle aspect ratio for Splash/Wide by centering
        if filename in ["Wide310x150Logo.png", "SplashScreen.png"]:
            canvas = Image.new("RGBA", size, (0, 0, 0, 0))
            # Resize icon to fit height
            scale = size[1] / img.height
            new_img = img.resize((int(img.width * scale), int(img.height * scale)), Image.Resampling.LANCZOS)
            x = (size[0] - new_img.width) // 2
            canvas.paste(new_img, (x, 0))
            canvas.save(os.path.join(output_dir, filename))
        else:
            img.resize(size, Image.Resampling.LANCZOS).save(os.path.join(output_dir, filename))
            
    print(f"MSIX Assets generated in {output_dir}")

    # Generate icon.ico for the EXE
    icon_path = os.path.join(os.path.dirname(source_path), "icon.ico")
    img.save(icon_path, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print(f"Executable Icon generated at {icon_path}")

if __name__ == "__main__":
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    generate_assets(os.path.join(assets_dir, "icon.png"), os.path.join(os.path.dirname(__file__), "MSStore_Assets"))
