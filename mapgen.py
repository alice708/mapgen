import subprocess

import numpy as np
from PIL import Image
import yaml
import os
import cv2

IMAGE_PATH = 'images/'

def main():
    config = yaml.safe_load(open("config.yaml"))
    colours = yaml.safe_load(open("colours.yaml"))

    size_x = config["size"]["x"]
    size_y = config["size"]["y"]

    array = np.zeros((size_y, size_x, 3), dtype=np.uint8) # y rows and x columns, 3 channels for RGB

    for x in range(size_x):
        for y in range(size_y):
            generate_pixel(config, colours, array, x, y, size_x, size_y)
        if x % config["freq"] == 0:
            # Save 
            new_image = Image.fromarray(array)
            new_image.save(f"{IMAGE_PATH}{x}.png")

    final = Image.fromarray(array)
    final.save("final.png")
    
    generate_video(config)
    
def generate_pixel(config, colours, array, x, y, size_x=None, size_y=None):
    # Just make a nice gradient for now
    array[y, x] = [255*y//size_y, 255*x//size_x,255*(size_y-y)//size_y]

def generate_video(config):
    image_folder = IMAGE_PATH
    video_name = 'timelapse.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith((".jpg", ".jpeg", ".png"))]
    images.sort(key=lambda x: int(os.path.splitext(x)[0]))  # Sort images by filename (assuming they are named as numbers)
    print("Images:", images)

    # Set frame from the first image
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    # Video writer to create .avi file
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), config["fps"], (width, height))

    # Appending images to video
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    # Release the video file
    video.release()
    cv2.destroyAllWindows()
    print("Video generated successfully!")

    subprocess.Popen(["/mnt/c/Program Files/VideoLAN/VLC/vlc.exe", video_name])


if __name__ == '__main__':
  main()