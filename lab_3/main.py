import os
import argparse
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np



def histogram(image_name: str) -> None:
    """
    Plots the histogram of an image showing the distribution of pixel intensities
    for each color channel (Red, Green, Blue).

    args:
    image_name (str): The path to the image file to analyze.
    """
    img = cv.imread(image_name)
    assert image_name is not None, "File doesnt found"
    print("Image size: ", img.shape)
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        hist = cv.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(hist, color=col)
        plt.xlim([0, 256])
    plt.xlabel('Intensity')
    plt.ylabel('Number of pixels')
    plt.title('Histogram')
    plt.legend(('Blue', 'Green', 'Red'), loc='upper left')
    plt.show()



def work_with_image(image_name: str, new_image_path: str) -> None:
    """
    Processes an image by inverting its color channels (creating a negative effect),
    displays the processed image, and saves it to the specified directory.

    args:
    image_name (str): The path to the image file to process.
    new_image_path (str): The directory where the processed image will be saved.
    """
    img = cv.imread(image_name, cv.IMREAD_COLOR)
    b, g, r = cv.split(img)
    b = 255 - b
    g = 255 - g
    r = 255 - r
    new_image = cv.merge((r, g, b))
    plt.imshow(new_image)
    plt.show()
    if not os.path.isdir(new_image_path):
        os.makedirs(new_image_path)
    result = os.path.join(new_image_path, "new_image.jpg")
    cv.imwrite(result, new_image)



def main() -> None:
    """
    Handle  arguments parsing and runs the histogram
    and image processing functions
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('image_name', type = str)
    parser.add_argument('new_image_path', type = str)
    args = parser.parse_args()
    histogram(args.image_name)
    work_with_image(args.image_name, args.new_image_path)



if __name__ == "__main__":
    main()
