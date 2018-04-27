# Used to save tests
import pickle
# This is used to log errors
from log_errors_info import *


def save_test_file(words, TESTS_FOLDER):
    ''' Saves the words and defintions into a file
        returns the code for the test '''
    code = get_code(words)
    filename = TESTS_FOLDER + code + '.test'
    with open(filename, 'wb') as fp:
        pickle.dump(words, fp)
    return code


def load_test_file(code, TESTS_FOLDER, ERROR_FOLDER):
    ''' Loads the file and defintions from a given code
        returns NONE if file not found or a dict of words and definitions '''
    words = None
    filename = TESTS_FOLDER + code + '.test'
    try:
        with open(filename, 'rb') as fp:
            words = pickle.load(fp)
    except Exception as e:
        log_file_error('File for code: ' + code + " doesn't exist. " + str(e))
    return words


def get_code(words):
    ''' Generates the code based on the words
        returns the generated code '''
    total_length = len(words)
    words_keys = words.keys()
    fwfl = words_keys[0][0]
    fwll = words_keys[0][-1]
    lwfl = words_keys[-1][0]
    lwll = words_keys[-1][-1]
    ascii_value = 0
    for word in words_keys:
        ascii_value = ascii_value + ord(word[0])
    return str(total_length) + fwfl + fwll + lwfl + lwll + str(ascii_value)
