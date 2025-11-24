import os
import cv2
from tqdm import tqdm
import json
import pandas as pd
from utils.logger import setup_logger
logger = setup_logger(log_file="main.log")

def process_videos():
    # Read checkpoint
    checkpoint_file = 'checkpoints/preprocess.json'
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint = json.load(f)
    else:
        checkpoint = {}

    if checkpoint.get('quality_check') != 'passed':
        # Create necessary directories
        os.makedirs('dataset/processed', exist_ok=True)

        # Quality check: Find videos with FPS over 30 and unopenable videos
        all_fps_over_30 = []
        unopen_videos = []

        root_dir = 'dataset/raw'
        for root, dirs, files in tqdm(os.walk(root_dir)):
            for video_file in files:
                if not video_file.endswith('.mp4'):
                    continue

                video_path = os.path.join(root, video_file)
                video = cv2.VideoCapture(video_path)

                if not video.isOpened():
                    unopen_videos.append(video_path)
                    continue

                fps = video.get(cv2.CAP_PROP_FPS)

                if fps > 30:
                    all_fps_over_30.append({'path': video_path, 'fps': fps})
                video.release()

        if len(unopen_videos) > 0:
            logger.error("An error happened. Some videos could not be opened.")
            print("Unopenable videos:")
            for path in unopen_videos:
                print(path)
            print("\nPlease repair the files above before proceeding.")
            sys.exit()

        for item in all_fps_over_30:
            print(f"Path: {item['path']}, FPS: {item['fps']}")
            print("\nPlease resample these videos to 30 FPS before proceeding.")
            logger.error("An error happened. Some videos are over 30 FPS. Need to resample these to 30 FPS")
            sys.exit()

        checkpoint['quality_check'] = 'passed'
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f)

    # Process videos
    if checkpoint.get('preprocessing') != 'completed':
        for root, dirs, files in tqdm(os.walk(root_dir)):
            for video_file in files:
                if not video_file.endswith('.mp4'):
                    continue

                video_path = os.path.join(root, video_file)
                video = cv2.VideoCapture(video_path)

                # Prepare output folder per each video file (name without extension)
                video_name = os.path.splitext(video_file)[0]
                output_dir = os.path.join('dataset/processed', video_name)
                os.makedirs(output_dir, exist_ok=True)

                frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
                frame_rate = int(fps)

                for i in range(frame_count):
                    ret, frame = video.read()
                    if not ret:
                        break
                    frame_filename = os.path.join(output_dir, f'frame_{i:05d}.jpg')
                    cv2.imwrite(frame_filename, frame)

                video.release()
        checkpoint['preprocessing'] = 'completed'
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f)

    # Extract each directory into video metadata file
    if checkpoint.get('video_metadata') != 'created':
        directories = os.listdir('dataset/processed')
        metadata = []
        for dir_name in tqdm(directories):
            thelist = dir_name.split(sep="_")
            total_frames = len(os.listdir(os.path.join('dataset/processed', dir_name)))
            metadata.append({
                "video_id": dir_name, "path": os.path.join('dataset/processed', dir_name), 
                "participant_id": thelist[0], "person_pose": thelist[1], "camera_pose": thelist[2],
                "category": thelist[3], "class_label": thelist[4], "frame_count": total_frames
            })
        
        df = pd.DataFrame(metadata)

        #####################################################
        ######## Remove "finish" signs due to error #########
        #####################################################
        df = df[df['class_label'] != 'finish']
        df.to_csv('dataset/processed/video_metadata.csv', index=False)

        checkpoint['video_metadata'] = 'created'
        with open(checkpoint_file, 'w') as f:
            json.dump(checkpoint, f)

if __name__ == "__main__":
    process_videos()