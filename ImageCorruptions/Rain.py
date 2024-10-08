import cv2
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFilter
from imgaug import augmenters as iaa
from matplotlib import pyplot as plt


def add_rain(image, severity):
    # linear interpolation between minimum value and max value in order to represent the five different severities
    x1, y1 = 1, 0.005   # min value
    x2, y2 = 5, 0.08    # max value
    x = severity
    severity = y1 + (y2 - y1) * (x - x1) / (x2 - x1)

    seq = iaa.Sequential(iaa.RainLayer(
            density=(severity),
            density_uniformity=(0),
            drop_size=(0.5),
            drop_size_uniformity=(0),
            angle=(-30, 30),
            seed=None,
            speed=(0.007, 0.03),
            blur_sigma_fraction=(0.0001, 0.001),
            random_state="deprecated",
            deterministic="deprecated"
        ))
    return np.asarray(seq(images=image))


if __name__ == "__main__":

    image = r"C:\Users\Bella\Documents\Codes\DataSet\Test_Dataset\images\adapter_plate_triangular000004.jpg"
    imgobj = cv2.imread(image)
    corrupted = add_rain(imgobj, 1)
    cv2.imshow('Fisheye Distorted Image', corrupted)
    cv2.waitKey(0)