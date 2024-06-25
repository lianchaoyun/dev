from datetime import time
from time import sleep
from moviepy.editor import VideoFileClip
import G

def get_preview_image(video_path, image_path):
    video = VideoFileClip(video_path)
    video.save_frame(image_path, t=10)
    print(video.size)
    total_frames = video.duration * video.fps
    print(f"Total frames: {total_frames}")

#  nohup python main.py &   tail -f nohup.out
if __name__ == '__main__':
    pass


video_path = 'C:\project\data\moe\Pinterest.mp4'  # 视频文件路径
image_path = 'preview.jpg'    # 预览图保存路径

get_preview_image(video_path, image_path)
