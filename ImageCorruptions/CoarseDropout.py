import albumentations as A
import cv2
import numpy as np


def coarse_dropout(image, severity=1):
    img_height = np.shape(image)[0]
    img_width = np.shape(image)[1]
    # Declare an augmentation pipeline
    transform = A.Compose([A.CoarseDropout(max_holes=20*severity,
                                           max_height=round(0.04*img_height),
                                           max_width=round(0.04*img_width),
                                           min_holes=5*severity,
                                           min_height=round(0.01*img_height),
                                           min_width=round(0.01*img_width),
                                           fill_value=0,
                                           mask_fill_value=None,
                                           always_apply=True,
                                           p=0.5)])

    # Augment an image
    transformed = transform(image=image)
    return transformed["image"]


if __name__ == "__main__":
    Path = r"C:\Users\Bella\Documents\Codes\DataSet\Test_Dataset\images\adapter_plate_triangular000004.jpg"
    image = cv2.imread(Path)
    corrupted_image = coarse_dropout(image, 5)
    cv2.imshow('image', corrupted_image)
    cv2.waitKey(0)