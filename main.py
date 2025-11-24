import os
import sys
from preprocess.process import process_videos
from utils.logger import setup_logger


# Set up logger and verify data presence
logger = setup_logger(log_file="main.log")

data_required = [
    'dataset/processed/training',
    'dataset/processed/validation',
    'dataset/processed/testing'
]

if not all(os.path.isdir(path) for path in data_required):
    if not os.path.exists('dataset/raw'):
        logger.error("Raw dataset not found. Please download the data from Panoptic and place it in 'dataset/raw'.")
        sys.exit()
    process_videos()
    logger.info("Data preprocessing completed.")