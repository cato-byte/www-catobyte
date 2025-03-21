from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path
# Create a new image with RGB mode, deep blue background, and 1024x1024 resolution
img = Image.new('RGB', (1024, 1024), (0, 0, 139))  # RGB for deep blue (0, 0, 139)

# Initialize ImageDraw to draw on the image
draw = ImageDraw.Draw(img)

# Set the font size and load the default font
# You can replace the font file with any .ttf file path if you want custom fonts
font_size = 70
font = ImageFont.load_default(size=font_size)

# Define the text you want to add to the image
text = "20 Leading AI projects"

# Get the bounding box of the text to center it
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Calculate the position for the text to be centered
position = ((1024 - text_width) // 2, (1024 - text_height) // 2)

# Add the text to the image
draw.text(position, text, fill=(255, 255, 255), font=font)  # White text (255, 255, 255)

# Save the image as a WEBP file
WEB_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR =  os.path.join(WEB_DIR,'images')
img.save(os.path.join(IMAGES_DIR,"20_leading_ai_projects.webp"), "WEBP")


# Save the image as a WEBP file

