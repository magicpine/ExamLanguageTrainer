# Used to check files
import os.path
# Used for HTTPError
import urllib2
# Used to shuffle definitions
import random
# Used to use the api
from wordnik import *
# This is the conversion to text module
from conversion import *
# Used to log errors
from errors import *


# Used to access the API
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '972e0b90c32a7859fc4944c19a603e0a6cf53a45963d7ee42 '
client = swagger.ApiClient(apiKey, apiUrl)


# Public Variables
NUM_OF_RANDOM_DEF = 3


def get_text(filename, UPLOAD_FOLDER):
    ''' Opens up a file and converts it into a text file and reads it
        returns a string of all the text in the file '''
    # Depending the the file it needs to be changed how it gets
    # Converted into text
    if is_pdf(filename):
        convert_pdf_to_text(filename, UPLOAD_FOLDER)
    elif is_ppt(filename):
        convert_ppt_to_text(filename, UPLOAD_FOLDER)
    else:
        convert_doc_to_text(filename, UPLOAD_FOLDER)
    # Delete the uploaded file
    os.system('rm -f ' + UPLOAD_FOLDER + filename)
    # The new file is the same name just with the txt extention
    new_filename = filename.split('.')[0] + '.txt'
    # Sometimes it gets saved in the UPLOADS folder so just seeing
    # Where the file is
    if not os.path.isfile(new_filename):
        new_filename = UPLOAD_FOLDER + new_filename
    # Open the file and get text
    try:
        with open(new_filename, 'r') as myfile:
            data = myfile.read().replace('\n', '')
    except Exception as e:
        err = 'Cannot read the text file of: ' + filename + ' ' + str(e)
        log_file_error(err)
        return 'ERROR'
    # Delete the new files and return the string of words
    os.system('rm -f ' + new_filename)
    return data


def allowed_file(filename, ALLOWED_EXTENSIONS):
    ''' Sees if the file extention is in the ALLOWED_EXTENSIONS
        returns True if it is, False if it isn't '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def split_text(data, DISALLOWED_WORD_LIST):
    ''' Splits the string into indiviual words and removes everything
        but numbers and letters
        returns a set of words '''
    # Remove the tabs
    data = data.replace('\t', '')
    data_list = data.split(' ')
    clean_list = []
    for word in data_list:
        # Needed for UTF-8 characters
        if not word.startswith("/"):
            for dwl in DISALLOWED_WORD_LIST:
                word = word.replace(dwl, ' ')
            # removes the \ (UTF-8) punctuation
            word = word.decode('utf-8', 'ignore')
            word = word.strip()
            # Words might have muilptle words in them due to formatting
            if len(word.split()) > 1:
                for split_word in word.split():
                    clean_list.append(split_word.strip())
            else:
                clean_list.append(word)
    clean_list_set = set(clean_list)
    clean_list_set_list = list(clean_list_set)
    return clean_list_set_list


def get_uncommon_words(data_list, FREQUENCY_LIMIT):
    ''' Determines which of the words are uncommon
        returns a set of words that are below the limit '''
    data_list_freq = {}
    # API
    wordApi = WordApi.WordApi(client)
    for word in data_list:
        try:
            freq = wordApi.getWordFrequency(word)
            if freq.totalCount <= FREQUENCY_LIMIT and freq.totalCount > 0:
                data_list_freq[word] = freq.totalCount
        except urllib2.HTTPError as e:
            # When the word doesn't exist, it throws a HTTP Error
            message = 'The word: ' + word + " doesn't exist. " + str(e)
            log_API_error(message)
            pass
        except urllib2.URLError as e:
            # API stops responding
            message = 'The API has stopped responding'
            log_API_error(message)
            return None
    return data_list_freq


def get_definitions(data_list_freq):
    ''' Takes a list of words and finds the definintions for the words it Can
        returns a dic of [word] = definition '''
    data_list_def = {}
    # API
    wordApi = WordApi.WordApi(client)
    for word in data_list_freq.keys():
        try:
            # The dictonary requires ascii characters
            word = word.decode('ascii', 'ignore')
            defin = wordApi.getDefinitions(word)
            # The API returns it as NONE if not found
            if (defin is not None):
                if (len(defin) > 0):
                    data_list_def[word] = defin[0].text
        except Exception as e:
            message = 'The word: ' + word + ' Threw a error. ' + str(e)
            log_API_error(message)
            pass
    return data_list_def


def get_random_defintions(length):
    ''' Gets random words and defintions the total being
        length * NUM_OF_RANDOM_DEF
        returns a dictonary of [word] = definition '''
    # for multiple choice test
    total_count = length * NUM_OF_RANDOM_DEF
    random_defintions = []
    wordsApi = WordsApi.WordsApi(client)
    wordApi = WordApi.WordApi(client)
    for x in range(total_count):
        example = wordsApi.getRandomWord(hasDictionaryDef=True,
                                         minDictionaryCount=2)
        exampleDef = wordApi.getDefinitions(example.word)
        # Recieve only the first defintion
        random_defintions.append(exampleDef[0].text)
    return random_defintions


def make_questions(data_list_def, list_random_def):
    ''' Makes a test by taking one word from the data_list_def
        and NUM_OF_RANDOM_DEF words from list_random_def to make a test
        returns a dictonary for the [word] = list of defintions '''
    questions = {}
    count = 0
    definitions = []
    for word in data_list_def:
        for x in range(NUM_OF_RANDOM_DEF):
            definitions.append(list_random_def[count])
            count = count + 1
        definitions.append(data_list_def[word])
        # randomize the defintions everytime
        random.shuffle(definitions)
        questions[word] = definitions
        definitions = []
    return questions
