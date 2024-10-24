import re
import argparse

def get_file()->str:
    """
    Get the filename from command-line arguments
    Raises SyntaxError if no filename is provided
    """
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('filename', type=str)
        return parser.parse_args().filename
    except:
        raise SyntaxError("Path is empty")

def open_file(str)->str:
    """
    Open and read the content of the file
    Raises FileNotFoundError if the file cannot be found
    """
    try:
        with open(str, "r", encoding="UTF-8") as file:
            return file.read()
    except:
        raise FileNotFoundError("File doesnt found or doesnt exist")

def find_fm_names(text)->list:
    """
    Extract female names starting with 'А' from the text
    Returns a list of unique names
    """
    pattern = r'Имя: А\w+\nПол: Ж'
    names = ''.join(re.findall(pattern, text))
    pattern = r'А\w+'
    answ = re.findall(pattern, names)
    answ = list(set(answ))
    return answ



if __name__ == "__main__":
    filename = get_file()
    text = open_file(filename)
    print(' '.join(find_fm_names(text)))
