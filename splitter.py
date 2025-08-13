# =============================================================================
# SCRIPT: AUTOMATED DATASET SPLITTER FOR YOLO
# =============================================================================
#
# DESCRIPTION:
# This script takes a folder of images and a folder of corresponding YOLO .txt
# labels and automatically splits them into training and validation sets,
# creating the required folder structure for YOLO training.
#
# REQUIREMENTS:
# - Python 3
#
# HOW TO USE:
# 1. Update the four paths/variables in the "CONFIGURATION" section below.
# 2. Run the script from your terminal: python your_script_name.py
#
# =============================================================================

import os
import random
import shutil

# =============================================================================
# --- CONFIGURATION (UPDATE THESE) ---
# =============================================================================

# 1. Path to the folder containing your original images.
source_images_folder = 'C:/Users/user/Downloads/Kvasir/Kvasir-SEG/Kvasir-SEG/images'

# 2. Path to the folder containing your generated .txt label files.
source_labels_folder = 'C:/Users/user/OneDrive/Desktop/yolo_labels'

# 3. Path to the new main folder where the final dataset will be created.
#    The script will create this folder for you.
output_dataset_folder = 'C:/Users/user/OneDrive/Desktop/polyp_dataset'

# 4. Split ratio for training data (e.g., 0.8 means 80% for training)
train_split_ratio = 0.8

# =============================================================================
# --- SCRIPT LOGIC (NO NEED TO EDIT BELOW THIS LINE) ---
# =============================================================================

def split_dataset():
    """
    Splits the dataset into training and validation sets and creates the
    necessary folder structure.
    """
    print("Starting dataset split...")

    # --- 1. Create the required directory structure ---
    train_images_path = os.path.join(output_dataset_folder, 'images', 'train')
    val_images_path = os.path.join(output_dataset_folder, 'images', 'val')
    train_labels_path = os.path.join(output_dataset_folder, 'labels', 'train')
    val_labels_path = os.path.join(output_dataset_folder, 'labels', 'val')

    # Create all directories if they don't exist
    os.makedirs(train_images_path, exist_ok=True)
    os.makedirs(val_images_path, exist_ok=True)
    os.makedirs(train_labels_path, exist_ok=True)
    os.makedirs(val_labels_path, exist_ok=True)
    print("Created folder structure.")

    # --- 2. Get the list of all images and shuffle them ---
    all_images = [f for f in os.listdir(source_images_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(all_images) # Shuffling is crucial for unbiased sets!
    print(f"Found {len(all_images)} images to process.")

    # --- 3. Calculate the split index ---
    split_index = int(len(all_images) * train_split_ratio)

    # --- 4. Split the list of images ---
    train_images = all_images[:split_index]
    val_images = all_images[split_index:]
    print(f"Splitting into {len(train_images)} training images and {len(val_images)} validation images.")

    # --- 5. Copy files to their new homes ---
    def copy_files(file_list, image_dest, label_dest):
        for filename in file_list:
            # Get the base name of the file without extension
            base_filename = os.path.splitext(filename)[0]
            
            # Define source paths for image and label
            image_src_path = os.path.join(source_images_folder, filename)
            label_src_path = os.path.join(source_labels_folder, base_filename + '.txt')

            # Define destination paths
            image_dest_path = os.path.join(image_dest, filename)
            label_dest_path = os.path.join(label_dest, base_filename + '.txt')

            # Copy the files, checking if the label exists
            if os.path.exists(label_src_path):
                shutil.copyfile(image_src_path, image_dest_path)
                shutil.copyfile(label_src_path, label_dest_path)
            else:
                print(f"Warning: Label for {filename} not found. Skipping this file.")

    print("\nCopying training files...")
    copy_files(train_images, train_images_path, train_labels_path)
    
    print("\nCopying validation files...")
    copy_files(val_images, val_images_path, val_labels_path)

    print("\n=============================================")
    print("Dataset splitting complete!")
    print(f"Final dataset created at: {output_dataset_folder}")
    print("=============================================")

# Run the main function
if __name__ == "__main__":
    split_dataset()
