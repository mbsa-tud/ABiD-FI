import numpy as np
import cv2


def chromatic_aberration(image, severity=1):

    image = np.array(image)
    b, g, r = cv2.split(image)

    shift = severity + 1  # adjust this value to control the amount of chromatic aberration

    b_shifted = np.roll(b, shift, axis=1)  # shift blue channel to the right
    g_shifted = np.roll(g, 0, axis=0)  # shift green channel upwards
    r_shifted = np.roll(r, -shift, axis=1)  # shift red channel downwards
    shifted_img = cv2.merge([b_shifted, g_shifted, r_shifted])
    return shifted_img
