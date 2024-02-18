## PS3-1 Image Improvement via area-to-pixel filers
import cv2
import numpy as np
import os

# User input feature
user_input = input("Please name your input color file: ")
file_directory = os.getcwd()
image_location = os.path.join(file_directory, user_input)
if os.path.exists(image_location):
    print(f"Your '{user_input}' image loaded successfully.")
    input_image = cv2.imread(user_input)
    cv2.imshow(f"'{user_input}'", input_image)
    cv2.waitKey(0)
else:
    print(f"Error: unable to load your input image.\nPlease make sure '{user_input}' is in the correct directory.")
    exit()

# Filtering process
input_image = cv2.imread(user_input)
# Different filtering combination for rainbow (bilateral+sharpening)
if user_input == 'rainbow.png':
    # smoothed_image = cv2.GaussianBlur(input_image, (5, 5), 0)
    smoothed_image = cv2.bilateralFilter(input_image, d=9, sigmaColor=75, sigmaSpace=75)
    kernel = 1
    sharpening_kernel = kernel * np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened_image = cv2.filter2D(smoothed_image, -1, sharpening_kernel)

# Different filtering combination for all other images (median+sharpening)
else:
    smoothed_image = cv2.medianBlur(input_image, 5)
    kernel = 1
    sharpening_kernel = kernel * np.array([[-1, -1, -1], [-1,  9, -1], [-1, -1, -1]])
    sharpened_image = cv2.filter2D(smoothed_image, -1, sharpening_kernel)

# Saving the output image
cv2.imshow(f"'{user_input}'", sharpened_image)
output_image = user_input.split('.')[0] + '-improved.' + user_input.split('.')[-1]
cv2.waitKey(0)
cv2.imwrite(output_image, sharpened_image)

cv2.destroyAllWindows()