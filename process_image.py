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
        
    # Resize
    height, width = img.shape[:2]
    new_width = 350
    new_height = int((new_width / width) * height)
    img = cv2.resize(img, (new_width, new_height))
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Green range
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([90, 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    
    mask_inv = cv2.bitwise_not(mask)
    # Erode the person mask to remove all green edge fringes
    mask_inv = cv2.erode(mask_inv, kernel, iterations=1)
    mask_inv = cv2.GaussianBlur(mask_inv, (3, 3), 0)
    
    b, g, r = cv2.split(img)
    rgba = cv2.merge([r, g, b, mask_inv])
    
    # 3D Dotted Mosaic Effect
    frames = []
    
    grid_size = 3  # Tighter spacing for much higher resolution
    radius = 1.5   # Constant size so the dark hoodie stays solid
    
    # Precalculate all dots
    dots = []
    for y in range(0, new_height, grid_size):
        row_dots = []
        for x in range(0, new_width, grid_size):
            # Check mask
            if mask_inv[y, x] > 50: # if not transparent
                color = rgba[y, x].tolist() # [r, g, b, a]
                row_dots.append((x, y, radius, tuple(color)))
        if row_dots:
            dots.append(row_dots)
            
    print("Generating frames...")
    
    # Base transparent canvas
    canvas = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Add initial frames
    for _ in range(5):
        frames.append(canvas.copy())
        
    # Print row by row
    frame_counter = 0
    for row in dots:
        # Draw this row
        for x, y, r, color in row:
            # Draw a slight drop shadow for 3D effect
            draw.ellipse([x-r+1, y-r+1, x+r+1, y+r+1], fill=(0,0,0,100))
            # Draw the actual dot
            draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
            
        # Save a frame every 3 rows for a smooth printing speed
        frame_counter += 1
        if frame_counter % 3 == 0:
            frames.append(canvas.copy())
            
    # Add final frame multiple times to pause at the end
    for _ in range(20):
        frames.append(canvas.copy())
        
    print("Saving GIF...")
    frames[0].save(
        'animated_profile.gif',
        format='GIF',
        save_all=True,
        append_images=frames[1:],
        duration=30,
        loop=0,
        disposal=2,
        transparency=0
    )
    print("Done!")

if __name__ == "__main__":
    process()
