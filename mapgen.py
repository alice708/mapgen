import numpy as np
from PIL import Image
import yaml


def main():
    config = yaml.safe_load(open("config.yaml"))
    colours = yaml.safe_load(open("colours.yaml"))

    size_x = config["size"]["x"]
    size_y = config["size"]["y"]

    array = np.zeros((size_x, size_y, 3))

    array = np.array(array, dtype=np.uint8)

    array[0,0] = [254,0,0]       # Makes the middle pixel red
    array[1,0] = [0,0,255]       # Makes the next pixel blue

    new_image = Image.fromarray(array)
    new_image.save('new.png')


if __name__ == '__main__':
  main()