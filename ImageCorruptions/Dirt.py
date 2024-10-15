import cv2
import numpy as np
import random
from PIL import Image


def add_dirt(image, severity):
    mask = get_mask(image, severity)

    # Convert the mask to a NumPy array and ensure it matches the image type
    mask = np.asarray(mask).astype(np.uint8)

    # Ensure the mask has the same number of channels as the image (3 channels for RGB)
    if len(mask.shape) == 2:  # If mask is grayscale
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Ensure the image and mask have the same shape
    if image.shape != mask.shape:
        raise ValueError("Image and mask must have the same shape.")

    # Perform the bitwise AND operation
    return cv2.bitwise_and(image, mask)


def get_mask(image, severity):
    overlay_path = rf"ImageCorruptions\dirt_samples/{severity}.jpg"
    mask = Image.open(overlay_path)

    img_height, img_width = np.shape(image)[:-1]  # Get image dimensions

    crop_width = img_width
    crop_height = img_height

    if crop_width > mask.size[0] or crop_height > mask.size[1]:
        mask = mask.resize((max(crop_width, mask.size[0]), max(crop_height, mask.size[1])))

    # Randomly crop the mask
    x = random.randint(0, mask.size[0] - crop_width)
    y = random.randint(0, mask.size[1] - crop_height)

    cropped_mask = mask.crop((x, y, x + crop_width, y + crop_height))

    return cropped_mask

r"""if __name__ == "__main__":
    photo_path = C:\Users\ac140891\PycharmProjects\FaultInjectionABiD\Test_Images/1726834778787366323.png
    image = cv2.imread(photo_path)
    for i in range (1, 6, 1):
        result = add_dirt(image, i)
        cv2.imshow("result", result)
        cv2.waitKey(0)"""