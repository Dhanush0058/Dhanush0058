import cv2
import numpy as np
from PIL import Image, ImageDraw

def process():
    print("Loading image...")
    # Load and remove green screen
    img = cv2.imread('profile.jpg')
    if img is None:
        print("Error: Could not load profile.jpg")
        return
        
    # Resize first to speed up processing
    height, width = img.shape[:2]
    new_width = 300
    new_height = int((new_width / width) * height)
    img = cv2.resize(img, (new_width, new_height))
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Green range - optimized for the typical green screen in the photo
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Refine mask with morphology
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    mask_inv = cv2.bitwise_not(mask)
    mask_inv = cv2.GaussianBlur(mask_inv, (3, 3), 0)
    
    b, g, r = cv2.split(img)
    rgba = cv2.merge([r, g, b, mask_inv])
    
    pil_img = Image.fromarray(rgba)
    
    # Create the "printer" effect frames
    frames = []
    
    # The printer moves down chunk by chunk
    chunk_size = 8
    
    print("Generating frames...")
    # Add initial empty frames
    for _ in range(5):
        frames.append(Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0)))
        
    for y in range(0, new_height + chunk_size, chunk_size):
        # Create empty transparent frame
        frame = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
        
        # Crop the image up to y
        if y > 0:
            box = (0, 0, new_width, min(y, new_height))
            region = pil_img.crop(box)
            frame.paste(region, box)
            
        # Draw a "printer head" / scanline at the current y
        if y < new_height:
            draw = ImageDraw.Draw(frame)
            # Glowing cyan scanline
            draw.line([(0, y), (new_width, y)], fill=(0, 255, 255, 200), width=3)
            # Dotted line
            for x in range(0, new_width, 10):
                draw.rectangle([x, y, x+4, y+4], fill=(255, 255, 255, 255))
            
        frames.append(frame)
        
    # Add a few frames of the finished image at the end
    for _ in range(15):
        frames.append(pil_img)
        
    print("Saving GIF...")
    frames[0].save(
        'animated_profile.gif',
        format='GIF',
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        disposal=2,
        transparency=0
    )
    print("Done!")

if __name__ == "__main__":
    process()
