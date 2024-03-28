import os
from PIL import Image

webp_files = [i[:-5] for i in os.listdir(os.getcwd()) if i.endswith(".webp")]

for file in webp_files:
    init_img = Image.open(f"{file}.webp")
    init_img.save(f"converted/{file}.png", "png")

    img = Image.open(f"converted/{file}.png")
    img = img.resize((512, 512), Image.NEAREST)
  
    background = Image.new("RGB", (512, 512), (140, 132, 120))
    background.paste(img, (0, 0), img)
    background.save(f"converted/{file}.png")
