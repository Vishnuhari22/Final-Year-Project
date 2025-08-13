Real-Time Polyp Detection using YOLOv8This document provides a comprehensive guide to the object detection module of our final year project. The goal of this module is to train a state-of-the-art YOLOv8 model to detect colon polyps in real-time from colonoscopy images and videos.Workflow OverviewThe project follows a standard machine learning pipeline, which can be summarized in three main phases:Data Preparation: We start with the expert-annotated Kvasir-SEG dataset. We use Python scripts to automatically convert the provided segmentation masks into YOLO-compatible bounding box labels and then split the data into training and validation sets.Model Training: We leverage Google Colab's free GPU resources to train a YOLOv8 model on our prepared dataset. The entire training process is managed within a Colab notebook.Inference & Prediction: After training, we use the final trained model (best.pt) to run predictions on new, unseen colonoscopy videos to test its performance.Phase 1: Data PreparationThis phase is fully automated using two Python scripts. The goal is to convert the raw Kvasir-SEG dataset into the precise folder structure and label format that YOLO requires.1. Automated Label Generation (Mask to Bounding Box)We use the provided segmentation masks to automatically generate bounding box labels.converter.py Script:This script reads each mask, finds the polyp's outline, calculates the bounding box, and saves it as a .txt file.import os
import cv2

# --- CONFIGURATION ---
image_folder = 'path/to/Kvasir-SEG/images'
mask_folder = 'path/to/Kvasir-SEG/masks'
output_label_folder = 'path/to/yolo_labels' # A new, empty folder

# --- SCRIPT LOGIC ---
# ... (Full script logic as provided before) ...
2. Automated Dataset SplittingThis script takes the original images and the newly generated labels and splits them into train and val sets.splitter.py Script:import os
import random
import shutil

# --- CONFIGURATION ---
source_images_folder = 'path/to/Kvasir-SEG/images'
source_labels_folder = 'path/to/yolo_labels'
output_dataset_folder = 'path/to/polyp_dataset' # Final dataset folder
train_split_ratio = 0.8

# --- SCRIPT LOGIC ---
# ... (Full script logic as provided before) ...
Phase 2: Model Training (in Google Colab)We use Google Colab for its free GPU access, which dramatically speeds up training. The entire process is contained within a single .ipynb notebook.1. Setup in ColabUpload Data: The final polyp_dataset folder is zipped and uploaded to a shared Google Drive folder (Final-Year-Project-Data).Mount Drive & Unzip: The notebook first mounts the Google Drive and unzips the dataset into the fast Colab runtime.# Mount Drive
from google.colab import drive
drive.mount('/content/drive')

# Unzip dataset
!unzip -q /content/drive/MyDrive/Final-Year-Project-Data/polyp_dataset.zip -d /content/
Install Library: We install the ultralytics library.!pip install ultralytics
2. Configuration (polyp.yaml)A .yaml file is created within the notebook to tell YOLO where to find the data.import yaml
data = {
    'train': '/content/polyp_dataset/images/train',
    'val': '/content/polyp_dataset/images/val',
    'nc': 1,
    'names': ['polyp']
}
with open('polyp.yaml', 'w') as f:
    yaml.dump(data, f)
3. Training CommandThe training is initiated with a single command. We train for 100 epochs using the yolov8n (nano) model as a starting point.!yolo detect train data=polyp.yaml model=yolov8n.pt epochs=100 imgsz=640
Phase 3: Results and Inference1. Training ResultsAfter 100 epochs, the model achieved excellent performance on the validation set:Precision: 88.5%Recall: 93.0%mAP50-95: 75.7%The final trained model is saved as best.pt and is stored permanently in our shared Google Drive.2. Running Prediction on a New VideoTo run inference, we use the saved best.pt model from Google Drive. This avoids the need for re-training.# Download a test video from YouTube
!pip install yt-dlp
!yt-dlp -o 'test_video.mp4' -f 'bestvideo[ext=mp4][vcodec^=avc1]+...' 'YOUTUBE_URL'

# Run prediction using the saved model
!yolo detect predict model=/content/drive/MyDrive/Final-Year-Project-Data/best.pt source=test_video.mp4 save_codec='mp4v'
The save_codec='mp4v' argument is crucial to ensure the output video is saved in a highly compatible MP4 format suitable for sharing. The final video is saved in the /content/runs/detect/predict/ directory.
