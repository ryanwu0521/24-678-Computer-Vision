# PS3-2 Edge detection
import cv2
import numpy as np
import os

# Sobel Filter Function
def sobel_filter(grayscale_image_sobel):
    sobel_horizontal = 1 / 16 * np.array([[-1, -2, 0, 2, 1], [-2, -4, 0, 4, 2], [-3, -6, 0, 6, 3], [-2, -4, 0, 4, 2], [-1, -2, 0, 2, 1]])
    sobel_vertical = 1 / 16 * np.array([[1, 2, 3, 2, 1], [2, 4, 6, 4, 2], [0, 0, 0, 0, 0], [-2, -4, -6, -4, -2], [-1, -2, -3, -2, -1]])

    edge_horizontal = cv2.filter2D(grayscale_image_sobel, cv2.CV_64F, sobel_horizontal)
    edge_vertical = cv2.filter2D(grayscale_image_sobel, cv2.CV_64F, sobel_vertical)

    edge_magnitude = np.sqrt(edge_horizontal ** 2 + edge_vertical ** 2)
    edge_direction = np.arctan2(edge_vertical, edge_horizontal)

    return edge_magnitude, edge_direction

# Canny Edge Filter Function
def canny_edge_filter(grayscale_image_canny, threshold1, threshold2, aperture_size, l2_gradient):
    aperture_size = max(3, min(aperture_size, 7))
    aperture_size = aperture_size if aperture_size % 2 != 0 else aperture_size - 1

    canny_edge = cv2.Canny(grayscale_image_canny, threshold1, threshold2, apertureSize=aperture_size, L2gradient=l2_gradient)
    negate_canny_edge_image = 255 - canny_edge

    cv2.imshow('Canny Edges', negate_canny_edge_image)

    return negate_canny_edge_image

# main script with user input feature
user_input = input("Please name your input color file: ")
file_directory = os.getcwd()
image_location = os.path.join(file_directory, user_input)
if os.path.exists(image_location):
    print(f"Your '{user_input}' image loaded successfully.")
    input_image = cv2.imread(user_input)
    cv2.imshow(f"'{user_input}'", input_image)
    cv2.waitKey(0)

    # Executing Sobel filter function
    grayscale_image_sobel = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    edge_magnitude, edge_direction = sobel_filter(grayscale_image_sobel)

    max_edge_magnitude = np.max(edge_magnitude)
    min_edge_magnitude = np.min(edge_magnitude)

    if max_edge_magnitude != min_edge_magnitude:
        edge_magnitude_normalized = 255 * (edge_magnitude - min_edge_magnitude) / (
                    max_edge_magnitude - min_edge_magnitude)
    else:
        edge_magnitude_normalized = edge_magnitude

    edge_magnitude_normalized = edge_magnitude_normalized.astype(np.uint8)
    negate_sobel_image = 255 - edge_magnitude_normalized

    # Converting grayscale into binary image
    if user_input == 'cheerios.png':
        threshold_value = 195
    elif user_input == 'professor.png':
        threshold_value = 220
    elif user_input == 'gear.png':
        threshold_value = 155
    else:
        threshold_value = 240

    _, binary_sobel_image = cv2.threshold(negate_sobel_image, threshold_value, 255, cv2.THRESH_BINARY)

    # Showing and saving Sobel filtered results
    cv2.imshow(f"'{user_input}'", binary_sobel_image)
    output_image_sobel = user_input.split('.')[0] + '-sobel.' + user_input.split('.')[-1]
    cv2.imwrite(output_image_sobel, binary_sobel_image)
    cv2.waitKey(0)

    # Executing Canny edge filter function
    grayscale_image_canny = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    # Canny edge GUI
    cv2.namedWindow('Canny Edge GUI')
    cv2.createTrackbar('Threshold1', 'Canny Edge GUI', 0, 255, lambda x: None)
    cv2.createTrackbar('Threshold2', 'Canny Edge GUI', 0, 255, lambda x: None)
    cv2.createTrackbar('Aperture Size', 'Canny Edge GUI',3, 7, lambda x: None)
    cv2.createTrackbar('L2 Gradient', 'Canny Edge GUI', 0, 1, lambda x: None)

    while True:
        threshold1 = cv2.getTrackbarPos('Threshold1', 'Canny Edge GUI')
        threshold2 = cv2.getTrackbarPos('Threshold2', 'Canny Edge GUI')
        aperture_size = cv2.getTrackbarPos('Aperture Size', 'Canny Edge GUI')
        l2_gradient = cv2.getTrackbarPos('L2 Gradient', 'Canny Edge GUI')

        canny_edge_result = canny_edge_filter(grayscale_image_canny, threshold1, threshold2, aperture_size, l2_gradient)
        negate_canny_edge_image = 255 - canny_edge_result
        cv2.imshow('Canny Edges', canny_edge_result)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):  # If the space key is pressed
            output_image_canny = user_input.split('.')[0] + '-canny.' + user_input.split('.')[-1]
            cv2.imwrite(output_image_canny, canny_edge_result)
            print(f"Canny edge filter image saved as: {output_image_canny}")
            break
    cv2.destroyAllWindows()

else:
    print(f"Error: unable to load your input image.\nPlease make sure '{user_input}' is in the correct directory.")
    exit()