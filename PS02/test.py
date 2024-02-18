import cv2
import numpy as np
import os

user_input = input("Please name your input color file: ")
file_directory = os.getcwd()
image_location = os.path.join(file_directory, user_input)

if os.path.exists(image_location):
    print(f"Your '{user_input}' image loaded successfully.")

    image = cv2.imread(user_input, cv2.IMREAD_GRAYSCALE)
    cv2.imshow(f"'{user_input}'", image)
    cv2.waitKey(0)

    highest_pixel_value = np.max(image)
    lowest_pixel_value = np.min(image)

    color_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            grey_pixel_value = image[i, j]

            RGB = np.zeros(3, dtype=np.uint8)

            if grey_pixel_value <= lowest_pixel_value + (highest_pixel_value - lowest_pixel_value) / 4:
                RGB[0] = 255
                RGB[1] = int(255 * (grey_pixel_value) / ((highest_pixel_value - lowest_pixel_value) / 4))
                RGB[2] = 0

            elif grey_pixel_value <= lowest_pixel_value + (highest_pixel_value - lowest_pixel_value) / 2:
                RGB[0] = int(255 - 255 * (grey_pixel_value - lowest_pixel_value - (highest_pixel_value - lowest_pixel_value) / 4) / ((highest_pixel_value - lowest_pixel_value) / 4))
                RGB[1] = 255
                RGB[2] = 0

            elif grey_pixel_value <= lowest_pixel_value + 3 * (highest_pixel_value - lowest_pixel_value) / 4:
                RGB[0] = 0
                RGB[1] = int(255 * (grey_pixel_value - lowest_pixel_value - 2 * (highest_pixel_value - lowest_pixel_value) / 4) / ((highest_pixel_value - lowest_pixel_value) / 4))
                RGB[2] = 255

            else:
                RGB[0] = 0
                RGB[1] = int(255 - 255 * (grey_pixel_value - 3 * (highest_pixel_value - lowest_pixel_value) / 4) / ((highest_pixel_value - lowest_pixel_value) / 4))
                RGB[2] = 255

            if RGB[1] < 0:
                RGB[1] = 0
            elif RGB[1] > 255:
                RGB[1] = 255

            color_image[i, j] = RGB

    cv2.imshow(f"'{user_input}'", color_image)
    cv2.waitKey(0)

    print(f"The highest pixel value for '{user_input}' is: {highest_pixel_value}")
    print(f"The lowest pixel value for '{user_input}' is: {lowest_pixel_value}")

else:
    print(f"Error: unable to load your input image.\nPlease make sure '{user_input}' is in the correct directory.")
    exit()
