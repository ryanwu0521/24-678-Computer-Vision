# 24-678 Computer Vision for Engineers
# Ryan Wu (ID:weihuanw)
# PS05 Binary image processing - detecting blobs, contours, and central axes
# Due 11/3/2023 (Fri) 5 pm

# import necessary packages
import cv2
import numpy as np

# function for loading given images
def load_images(image_path1, image_path2):
    wall1_image = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    wall2_image = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)
    return wall1_image, wall2_image

# function for image dilation and erosion
def dilation_erosion(image, iterations=3):
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    erode_image = cv2.erode(image, kernel, iterations=iterations)
    dilate_image= cv2.dilate(erode_image, kernel, iterations=iterations)
    return dilate_image

# function for drawing contours
def blob_contours(image):
    # inverting the image
    inverted_image = cv2.bitwise_not(image)
    # funding contours using the inverted image
    contours, _ = cv2.findContours(inverted_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # converting the image back to BGR
    contour_image = cv2.cvtColor(inverted_image, cv2.COLOR_GRAY2BGR)
    # drawing contours on the image
    for contour in contours:
        color = tuple(np.random.randint(0, 255, 3).tolist())
        cv2.drawContours(contour_image, [contour], -1, color, 2)
    # converting the image back
    contour_image_color = cv2.bitwise_not(contour_image)
    # returning the image with contours
    return contour_image_color

# function for detecting cracks
def detect_crack_and_thin(image, contour_length_threshold = 2000):
    # inverting the image
    inverted_image = cv2.bitwise_not(image)
    crack_image = image.copy()
    # Finding contours
    contours, _ = cv2.findContours(inverted_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_crack = []
    # Filtering contours
    for contour in contours:
        # calculate contour arc length
        arc_length = cv2.arcLength(contour, True)

        # filter contours based on area
        if arc_length <= contour_length_threshold:
            contour_crack.append(contour)

    cv2.drawContours(crack_image, contour_crack, -1, (255, 255, 255), 10)

    # calling the thinning function
    thinned_crack_image = thinning(crack_image)

    return thinned_crack_image

# function for thinning
def thinning(image):
    # reverse image (black background)
    black_image = cv2.bitwise_not(image)
    # Kernel: 4 neighbor
    k_e = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    # Target image
    thin = np.zeros(black_image.shape, dtype=np.uint8)
    # repeat until no white area
    while cv2.countNonZero(black_image) != 0:
        er = cv2.erode(black_image, k_e)
        # OPEN: erosion then dilation (remove noise)
        op = cv2.morphologyEx(er, cv2.MORPH_OPEN, k_e)
        subset = cv2.subtract(er, op)
        thin = cv2.bitwise_or(subset, thin)
        black_image = er.copy()

    # invert the thinned image back to white background
    thinned_image = cv2.bitwise_not(thin)
    return thinned_image

# main function
def main():
    # calling load_images function
    wall1_image, wall2_image = load_images('wall1.png', 'wall2.png')
    if wall1_image is not None and wall2_image is not None:
        # calling dilation_erosion function
        wall1_blobed = dilation_erosion(wall1_image)
        wall2_blobed = dilation_erosion(wall2_image)

        # calling blob_contours function
        wall1_contoured = blob_contours(wall1_blobed)
        wall2_contoured = blob_contours(wall2_blobed)

        # calling detect_crack function (setting contour length threshold to 2000 for wall1 and 500 for wall2)
        wall1_thinned_crack_image = detect_crack_and_thin(wall1_blobed, contour_length_threshold=2000)
        wall2_thinned_crack_image = detect_crack_and_thin(wall2_blobed, contour_length_threshold=500)

        # display and save images
        # cv2.imshow('Wall 1 Image Blobs', wall1_blobed)
        # cv2.imshow('Wall 2 Image Blobs', wall2_blobed)
        cv2.imwrite("wall1-blobs.png", wall1_blobed)
        cv2.imwrite("wall2-blobs.png", wall1_blobed)

        # cv2.imshow('Wall 1 Image Contours', wall1_contoured)
        # cv2.imshow('Wall 2 Image Contours', wall2_contoured)
        cv2.imwrite("wall1-contours.png", wall1_contoured)
        cv2.imwrite("wall2-contours.png", wall2_contoured)

        # cv2.imshow('Wall 1 Crack Image', wall1_thinned_crack_image)
        # cv2.imshow('Wall 2 Crack Image', wall2_thinned_crack_image)
        cv2.imwrite("wall1-cracks.png", wall1_thinned_crack_image)
        cv2.imwrite("wall2-cracks.png", wall2_thinned_crack_image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error in loading wall images.")

# if __name__ == "__main__":
main()
