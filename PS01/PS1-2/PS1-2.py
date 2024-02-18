import cv2
import numpy as np
import os

# PS1-2 (1) User input feature
user_input = input("Please name your input color file: ")
file_directory = os.getcwd()
image_location = os.path.join(file_directory, user_input)
if os.path.exists(image_location):
    print(f"Your '{user_input}' image loaded successfully.")
else:
    print(f"Error: unable to load your input image.\nPlease make sure '{user_input}' is in the correct directory.")
    exit()

emphasize_choice = input("Please indicate your emphasize region, 'dark' or 'bright'?: ")
if emphasize_choice == 'dark':
    print(f"You choose '{emphasize_choice}' as your emphasize region .")
elif emphasize_choice == 'bright':
    print(f"You choose '{emphasize_choice}' as your emphasize region .")
else:
    print("Error: unable execute region emphasis.")
    exit()

# PS1-2 (1) Open and load image files
if user_input == 'circuit.png':
    circuit_color = cv2.imread(user_input)
    cv2.imshow('Circuit Color Image', circuit_color)
    cv2.waitKey(0)
    cv2.destroyWindow('Circuit Color Image')
elif user_input == 'crack.png':
    crack_color = cv2.imread(user_input)
    cv2.imshow('Crack Color Image', crack_color)
    cv2.waitKey(0)
    cv2.destroyWindow('Crack Color Image')

# PS1-2 (2) Convert color image to grayscale
if user_input == 'circuit.png':
    circuit_color = cv2.imread(user_input)
    circuit_grey = cv2.cvtColor(circuit_color, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Circuit Grey Image', circuit_grey)
    cv2.waitKey(0)
    cv2.destroyWindow('Circuit Grey Image')
    cv2.imwrite('circuit_grayscale.png', circuit_grey)
elif user_input == 'crack.png':
    circuit_color = cv2.imread(user_input)
    crack_grey = cv2.cvtColor(circuit_color, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Crack Grey Image', crack_grey)
    cv2.waitKey(0)
    cv2.destroyWindow('Circuit Grey Image')
    cv2.imwrite('crack_grayscale.png', crack_grey)

# PS1-2 (3) Convert greyscale image to binary
if user_input == 'circuit.png':
    circuit_grey = cv2.imread('circuit_grayscale.png', cv2.IMREAD_GRAYSCALE)
    _, circuit_binary = cv2.threshold(circuit_grey, 95, 255, cv2.THRESH_BINARY)
    cv2.imshow('Circuit Binary Image', circuit_binary)
    cv2.waitKey(0)
    cv2.destroyWindow('Circuit Binary Image')
    cv2.imwrite('circuit_binary.png', circuit_binary)
elif user_input == 'crack.png':
    crack_grey = cv2.imread('crack_grayscale.png', cv2.IMREAD_GRAYSCALE)
    _, crack_binary = cv2.threshold(crack_grey, 180, 255, cv2.THRESH_BINARY)
    cv2.imshow('Crack Binary Image', crack_binary)
    cv2.waitKey(0)
    cv2.destroyWindow('Crack Binary Image')
    cv2.imwrite('crack_binary.png', crack_binary)

# PS1-2 (4) Painting image pixel
# Circuit image color conversion
if user_input == 'circuit.png':
    circuit_color = cv2.imread(user_input)
    circuit_color_hsv = cv2.cvtColor(circuit_color, cv2.COLOR_BGR2HSV)
    lower_green = np.array([10, 100, 100])
    upper_green = np.array([20, 100, 100])
    lower_yellow = np.array([10, 85, 100])
    upper_yellow = np.array([70, 255, 255])

    mask_green = cv2.inRange(circuit_color_hsv, lower_green, upper_green)
    mask_yellow = cv2.inRange(circuit_color_hsv, lower_yellow, upper_yellow)
    mask_green_yellow_circuit = cv2.bitwise_or(mask_green, mask_yellow)
    mask_red_circuit = np.zeros_like(mask_green_yellow_circuit)
    if emphasize_choice == 'bright':
        mask_red_circuit[mask_green_yellow_circuit > 0] = 255
        circuit_output_image_bright = circuit_color.copy()
        circuit_output_image_bright[np.where(mask_red_circuit == 255)] = [0, 0, 255]

        cv2.imshow('Circuit Output Image (Bright)', circuit_output_image_bright)
        cv2.imwrite('circuit_output.png', circuit_output_image_bright)
        cv2.waitKey(0)
        cv2.destroyWindow('Circuit Output Image (Bright)')
    elif emphasize_choice == 'dark':
        mask_red_circuit[mask_green_yellow_circuit > 0] = 255
        circuit_output_image_dark = circuit_color.copy()
        circuit_output_image_dark[np.where(mask_red_circuit != 255)] = [0, 0, 255]

        cv2.imshow('Circuit Output Image (Dark)', circuit_output_image_dark)
        cv2.imwrite('circuit_output.png', circuit_output_image_dark)
        cv2.waitKey(0)
        cv2.destroyWindow('Circuit Output Image (Dark)')

# Crack image color conversion
elif user_input == 'crack.png':
    crack_color = cv2.imread(user_input)
    crack_color_hsv = cv2.cvtColor(crack_color, cv2.COLOR_BGR2HSV)
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 180, 180])

    mask_black = cv2.inRange(crack_color_hsv, lower_black, upper_black)
    mask_black_crack = cv2.bitwise_or(mask_black, mask_black)
    mask_red_crack = np.zeros_like(mask_black_crack)
    if emphasize_choice == 'bright':
        mask_red_crack[mask_black_crack > 0] = 255
        crack_output_image_bright = crack_color.copy()
        crack_output_image_bright[np.where(mask_black_crack != 255)] = [0, 0, 255]

        cv2.imshow('Crack Output Image (Bright)', crack_output_image_bright)
        cv2.imwrite('crack_output.png', crack_output_image_bright)
        cv2.waitKey(0)
        cv2.destroyWindow('Crack Output Image (Bright)')
    elif emphasize_choice == 'dark':
        mask_black_crack[mask_black_crack > 0] = 255
        crack_output_image_dark = crack_color.copy()
        crack_output_image_dark[np.where(mask_black_crack == 255)] = [0, 0, 255]

        cv2.imshow('Crack Output Image (Dark)', crack_output_image_dark)
        cv2.imwrite('crack_output.png', crack_output_image_dark)
        cv2.waitKey(0)
        cv2.destroyWindow('Crack Output Image (Dark)')
exit()