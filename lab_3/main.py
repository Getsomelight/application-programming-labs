import os
import argparse
from array import ArrayType
import cv2 as cv
import matplotlib.pyplot as plt



def histogram(img: ArrayType) -> None:
    """
    Plots the histogram of an image showing the distribution of pixel intensities
    for each color channel (Red, Green, Blue).

    args:
    img (ArrayType): The image.
    """
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


def inverting_image(img: ArrayType, new_image_path: str) -> None:
    """
    Processes an image by inverting its color channels (creating a negative effect),
    displays the processed image, and saves it to the specified directory.

    args:
    img (ArrayType): The image to process.
    new_image_path (str): The directory where the processed image will be saved.
    """
    b, g, r = cv.split(img)
    b = 255 - b
    g = 255 - g
    r = 255 - r
    new_image = cv.merge((r, g, b))
    plt.imshow(new_image)
    plt.show()
    os.makedirs(new_image_path, exist_ok = True)
    cv.imwrite(os.path.join(new_image_path, "new_image.jpg"), new_image)



def main() -> None:
    """
    Handle  arguments parsing and runs the histogram
    and image processing functions
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('image_name', type = str)
    parser.add_argument('new_image_path', type = str)
    args = parser.parse_args()
    img = cv.imread(args.image_name)
    assert args.image_name is not None, "File doesnt found"
    histogram(img)
    inverting_image(img, args.new_image_path)



if __name__ == "__main__":
    main()
