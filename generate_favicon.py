"""
Generate a simple favicon for PsyBot
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Create a 32x32 image with a purple gradient background
favicon = Image.new('RGB', (32, 32), color=(102, 126, 234))  # #667eea
draw = ImageDraw.Draw(favicon)

# Draw a simple avatar face
# Circle
draw.ellipse((8, 8, 24, 24), fill=(255, 255, 255))

# Eyes
draw.ellipse((12, 14, 15, 17), fill=(0, 0, 0))  # Left eye
draw.ellipse((17, 14, 20, 17), fill=(0, 0, 0))  # Right eye

# Smile
draw.arc((12, 14, 20, 21), start=0, end=180, fill=(0, 0, 0), width=1)

# Save as .ico file
favicon.save("static/favicon.ico")
print("Favicon created and saved to static/favicon.ico")
