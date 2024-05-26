import cv2
import numpy as np

def extract_panels(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Thresholding the image to make it binary
    _, thresh = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
    
    # Finding contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Initialize a list to hold the coordinates of each panel
    panels = []
    
    # Extract the bounding rectangles of each contour
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 50:  # Filter out too small contours that might not be panels
            panels.append((x, y, w, h))
    
    # Sort panels from top to bottom, and then right to left
    panels.sort(key=lambda b: (b[1], -b[0]))
    
    # Cropping and saving each panel
    panel_images = []
    for i, (x, y, w, h) in enumerate(panels):
        panel = image[y:y+h, x:x+w]
        panel_images.append(panel)
        cv2.imwrite(f'panel_{i}.png', panel)  # Save or display
    
    return panel_images

# Usage
panels = extract_panels('path_to_your_manga_page.jpg')
