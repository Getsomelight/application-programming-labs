import os
import numpy as np
import pandas as pd
import argparse
import cv2 as cv
import matplotlib.pyplot as plt



def make_dataframe(annotation_path: str) -> pd.DataFrame:
    """
    Creates a DataFrame based on annotations from a CSV file.

    args:
    annotation_path (str): Path to the CSV file with annotations.

    returns:
    pd.DataFrame: DataFrame containing absolute and relative paths to images, along with their width, height, and depth.
    """
    s = pd.DataFrame()
    df = pd.read_csv(annotation_path)
    for i in range (0, len(df), 2):
        s1 = pd.DataFrame({"Absolute": [""], "Relative": [""], "width": [""], "height": [""], "deep": [""]})
        s1["Absolute"] = df.iloc[i, 0]
        s1["Relative"] = df.iloc[i + 1, 0]
        a = "..\\" + df.iloc[i + 1, 0]
        img = cv.imread(a)
        s1["width"], s1["height"], s1["deep"] = img.shape
        s = pd.concat([s, s1], ignore_index=True)
    print(s)
    print(s.describe(include="int64"))
    return s


def sorted_dataframe(df: pd.DataFrame, max_width: int, max_height: int) -> pd.DataFrame:
    """
    Filters images with dimensions less than or equal to the specified width and height.
    Calculates the area (width * height) and sorts the DataFrame by this area.

    args:
    df (pd.DataFrame): Input DataFrame with image data.
    max_width (int): Maximum allowed image width.
    max_height (int): Maximum allowed image height.

    returns:
    pd.DataFrame: Sorted DataFrame with an additional column for area.
    """
    df = df[df['width'].apply(lambda x: x <= max_width)]
    df = df[df['height'].apply(lambda x: x <= max_height)]
    df = df.reindex(columns=list(df.columns) + ["area"])
    for i in range(0, len(df)):
        df.iloc[i, 5] = df.iloc[i, 2] * df.iloc[i, 3]
    df = df.sort_values(by="area")
    print(df)
    return df


def histogram(df: pd.DataFrame) -> None:
    """
    Creates a histogram of image area distribution.

    args:
    df (pd.DataFrame): DataFrame containing image data, including the area column.
    """
    df.hist(column = 'area')
    plt.xlabel('Area')
    plt.ylabel('quantity')
    plt.title('Histogram')
    plt.show()


def main() -> None:
    """
    Processes command-line arguments, creates a DataFrame from annotations,
    filters images by dimensions, sorts them, and displays a histogram
    of the area distribution.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('annotation_path', type = str)
    parser.add_argument('max_width', type = int)
    parser.add_argument('max_height', type = int)
    args = parser.parse_args()
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    assert args.annotation_path is not None, "File doesnt found"
    histogram(sorted_dataframe(make_dataframe(args.annotation_path), args.max_width, args.max_height))




if __name__ == "__main__":
    main()