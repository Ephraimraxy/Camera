"""
Create a simple icon for the application
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple application icon"""
    # Create a 64x64 icon
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a face-like icon
    # Face circle
    face_center = (size // 2, size // 2)
    face_radius = 20
    draw.ellipse([face_center[0] - face_radius, face_center[1] - face_radius,
                  face_center[0] + face_radius, face_center[1] + face_radius],
                 fill=(52, 152, 219, 255), outline=(41, 128, 185, 255), width=2)
    
    # Eyes
    eye_y = face_center[1] - 8
    draw.ellipse([face_center[0] - 8, eye_y - 3, face_center[0] - 4, eye_y + 3],
                 fill=(255, 255, 255, 255))
    draw.ellipse([face_center[0] + 4, eye_y - 3, face_center[0] + 8, eye_y + 3],
                 fill=(255, 255, 255, 255))
    
    # Nose
    draw.polygon([face_center[0], face_center[1] - 2,
                  face_center[0] - 2, face_center[1] + 2,
                  face_center[0] + 2, face_center[1] + 2],
                 fill=(41, 128, 185, 255))
    
    # Mouth
    draw.arc([face_center[0] - 6, face_center[1] + 2,
              face_center[0] + 6, face_center[1] + 10],
             0, 180, fill=(41, 128, 185, 255), width=2)
    
    # Save as ICO
    img.save('icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("✅ Icon created: icon.ico")

if __name__ == "__main__":
    create_icon()
