import argparse
import csv
import os
from icrawler.builtin import GoogleImageCrawler



class ImageIterator:
    def __init__(self, annotation: str):
        """
        Initializes the ImageIterator with a path to a CSV file

        args:
        annotation (str): Path to the CSV file containing image paths
        """
        with open(annotation, 'r') as annotation:
            read = csv.reader(annotation)
            self.data = [r for r in read]
            self.lim = len(self.data)
            self.count = 0

    def __iter__(self):
        """
        Returns the iterator object itself
        """
        return self

    def __next__(self):
        """
        Returns the next item in the iteration
        When the end of data is reached, raises StopIteration
        """
        if self.count < self.lim:
            currow =  "".join(self.data[self.count])
            self.count += 1
            return currow
        else:
            raise StopIteration



def img_download(search_name: str, folder: str) -> None:
    """
    Creates the folder if it doesn't exist
    Downloads images based on a search_name and saves them to a folder

    args:
    search_name (str): The search term to use for image downloading
    folder (str): Directory where the downloaded images will be stored
    """
    if not os.path.isdir(folder):
        os.makedirs(folder)
    crawler = GoogleImageCrawler(storage={"root_dir": folder})
    crawler.crawl(keyword=search_name, max_num=50)



def annotations(folder: str, annotation: str) -> None:
    """
    Create a CSV file with absolute and relative paths of image files
    Walks through the folder, finds image files, and writes their absolute and relative paths to the CSV file

    args:
    folder (str): The folder containing the images to annotate
    annotation (str): Path to the CSV file to store image paths
    """
    path = []
    for directory, space, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith(('.jpg', '.jpeg', '.webp', '.png')):
                path.append(os.path.join(directory, filename))
    with open(annotation, 'w', newline = '') as file:
        write = csv.writer(file)
        for path in path:
            abspath = os.path.abspath(path)
            relpath = os.path.relpath(path, start=os.path.dirname(annotation))
            write.writerow([abspath])
            write.writerow([relpath])



def main() -> None:
    """
    Handle argument parsing and execute image download, annotation, and iteration
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('search_name', type = str)
    parser.add_argument('folder', type = str)
    parser.add_argument('annotation', type = str)
    args = parser.parse_args()
    img_download(args.search_name, args.folder)
    annotations(args.folder, args.annotation)
    image_iterator = ImageIterator(args.annotation)
    for i in image_iterator:
        print(i)



if __name__ == "__main__":
    main()
