# =============================================================================
# SCRIPT: MASK TO YOLO ANNOTATION CONVERTER
# =============================================================================
#
# DESCRIPTION:
# This script reads black-and-white segmentation mask images, finds the object
# (the white area), calculates its bounding box, and saves the coordinates
# in the YOLO .txt format required for training object detection models.
#
# REQUIREMENTS:
# - Python 3
# - OpenCV library (install using: pip install opencv-python)
# - NumPy library (usually installed with OpenCV)
#
# HOW TO USE:
# 1. Install the required libraries.
# 2. Update the three folder paths in the "CONFIGURATION" section below.
# 3. Run the script from your terminal: python your_script_name.py
#
# =============================================================================

import os
import cv2
import numpy as np

# =============================================================================
# --- CONFIGURATION (CORRECTED PATHS) ---
# =============================================================================

# 1. Path to the folder containing your ORIGINAL color images.
#    We need these to get the correct image dimensions (width and height).
#    NOTE: Corrected the path to include the top-level "Kvasir" folder.
image_folder = 'C:/Users/user/Downloads/Kvasir/Kvasir-SEG/Kvasir-SEG/images'

# 2. Path to the folder containing the black-and-white MASK images.
#    The script will process every image in this folder.
#    NOTE: Corrected the path to include the top-level "Kvasir" folder.
mask_folder = 'C:/Users/user/Downloads/Kvasir/Kvasir-SEG/Kvasir-SEG/masks'

# 3. Path to the folder where you want to SAVE the new YOLO .txt label files.
#    Create a new, empty folder for this.
output_label_folder = 'C:/Users/user/OneDrive/Desktop/yolo_labels'

# =============================================================================
# --- SCRIPT LOGIC (NO NEED TO EDIT BELOW THIS LINE) ---
# =============================================================================

# Ensure the output directory exists
if not os.path.exists(output_label_folder):
    os.makedirs(output_label_folder)

# Loop through all the files in the mask folder
print(f"Starting conversion for masks in: {mask_folder}")
for mask_filename in os.listdir(mask_folder):
    # Process only image files (e.g., .png, .jpg)
    if mask_filename.endswith(('.png', '.jpg', '.jpeg')):
        
        # --- 1. Load the mask image ---
        mask_path = os.path.join(mask_folder, mask_filename)
        # Read the mask in grayscale (black and white)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        if mask is None:
            print(f"Warning: Could not read mask file: {mask_filename}")
            continue

        # --- 2. Get original image dimensions ---
        # We assume the original image has the same filename as the mask
        original_image_path = os.path.join(image_folder, mask_filename)
        if not os.path.exists(original_image_path):
            print(f"Warning: Original image not found for mask: {mask_filename}")
            continue
            
        original_image = cv2.imread(original_image_path)
        img_h, img_w, _ = original_image.shape

        # --- 3. Find contours in the mask ---
        # A "contour" is the outline of a shape. We are looking for the outline
        # of the white polyp shape in the black mask image.
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # --- 4. Get the bounding box from the largest contour ---
            # In case there are multiple small white spots, we take the largest one.
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)

            # --- 5. Normalize coordinates for YOLO format ---
            # YOLO format requires coordinates to be normalized from 0 to 1.
            # <x_center> <y_center> <width> <height>
            x_center_norm = (x + w / 2) / img_w
            y_center_norm = (y + h / 2) / img_h
            width_norm = w / img_w
            height_norm = h / img_h

            # --- 6. Save the YOLO .txt file ---
            # The output filename will be the same as the image, but with a .txt extension.
            output_filename = os.path.splitext(mask_filename)[0] + '.txt'
            output_path = os.path.join(output_label_folder, output_filename)

            with open(output_path, 'w') as f:
                # The '0' is the class ID. Since we only have one class (polyp), it's always 0.
                f.write(f"0 {x_center_norm:.6f} {y_center_norm:.6f} {width_norm:.6f} {height_norm:.6f}\n")
            
            print(f"Successfully converted: {mask_filename} -> {output_filename}")

        else:
            print(f"Warning: No contours found in mask: {mask_filename}")

print("=============================================")
print("Conversion complete!")
print(f"YOLO label files saved in: {output_label_folder}")
print("=============================================")
