import cv2
import numpy as np
from PIL import Image, ImageDraw

def process():
    print("Loading image...")
    img = cv2.imread('profile.jpg')
    if img is None:
        print("Error: Could not load profile.jpg")
        return
        
    height, width = img.shape[:2]
    new_width = 350
    new_height = int((new_width / width) * height)
    img = cv2.resize(img, (new_width, new_height))
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    mask_inv = cv2.bitwise_not(mask)
    mask_inv = cv2.GaussianBlur(mask_inv, (3, 3), 0)
    
    b, g, r = cv2.split(img)
    rgba = cv2.merge([r, g, b, mask_inv])
    
    pil_img = Image.fromarray(rgba)
    
    frames = []
    chunk_size = 6
    
    print("Generating frames...")
    # Add initial empty frames
    for _ in range(3):
        frames.append(Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0)))
        
    # Printer wipe effect
    for y in range(0, new_height + chunk_size, chunk_size):
        frame = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
        
        # Paste the image up to the current y (proper image, not abstract dots)
        if y > 0:
            box = (0, 0, new_width, min(y, new_height))
            region = pil_img.crop(box)
            frame.paste(region, box)
            
        # Draw the dotted 3D printer head (laser line + dots)
        if y < new_height:
            draw = ImageDraw.Draw(frame)
            draw.line([(0, y), (new_width, y)], fill=(51, 130, 237, 200), width=4) # Blue glow
            # Add printing dots
            for x in range(0, new_width, 8):
                draw.rectangle([x, y, x+3, y+3], fill=(250, 204, 21, 255)) # Yellow laser dots
            
        frames.append(frame)
        
    for _ in range(15):
        frames.append(pil_img)
        
    print("Saving GIF...")
    frames[0].save(
        'animated_profile.gif',
        format='GIF',
        save_all=True,
        append_images=frames[1:],
        duration=60,
        loop=0,
        disposal=2,
        transparency=0
    )
    print("Done!")

if __name__ == "__main__":
    process()
