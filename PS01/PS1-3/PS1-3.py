import cv2
import numpy as np
import os

# PS1-3 (3) Gamma correction Function
def gamma_correction(image_input, gamma=1.0):
    image_input = cv2.imread(user_input)
    gamma_table = np.array([((i/255) ** gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    output_image = cv2.LUT(image_input, gamma_table)
    return output_image

# PS1-3 (1) User input file
user_input = input("Please name your input color file: ")
file_directory = os.getcwd()
image_location = os.path.join(file_directory, user_input)
if os.path.exists(image_location):
    print(f"Your '{user_input}' image loaded successfully.")
    image_input = cv2.imread(user_input)
    cv2.imshow('Input image', image_input)
else:
    print(f"Error: unable to load your input image.\nPlease make sure '{user_input}' is in the correct directory.")
    exit()

# PS1-3 (2) (4) User input gamma correction; Saving final output files
user_gamma_value = input("Please indicate your desire gamma correction value: ")
gamma_value = float(user_gamma_value)
if gamma_value > 0:
    print(f"You choose '{gamma_value}' as your gamma correction value.")
    gamma_corrected_image = gamma_correction(user_input, gamma=gamma_value)
    cv2.imshow('Output image after gamma correction', gamma_corrected_image)
    final_image = user_input.split('.')[0] + '_gcorrected.' + user_input.split('.')[-1]
    cv2.imwrite( final_image, gamma_corrected_image)
    cv2.waitKey(0)
    cv2.destroyWindow('Circuit Color Image')
elif gamma_value < 0:
    print(f"'{gamma_value}' is an invalid gamma correction value.")
    exit()
else:
    print(f"'{gamma_value}' is an invalid gamma correction value.")
    exit()
exit()