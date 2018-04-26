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


apiUrl = 'http://api.wordnik.com/v4'
apiKey = '972e0b90c32a7859fc4944c19a603e0a6cf53a45963d7ee42 '
client = swagger.ApiClient(apiKey, apiUrl)


NUM_OF_RANDOM_DEF = 3


def get_text(filename, UPLOAD_FOLDER):
    # Depending the the file it needs to be changed how it gets
    # Converted into text
    if is_pdf(filename):
        convert_pdf_to_text(filename, UPLOAD_FOLDER)
    elif is_ppt(filename):
        convert_ppt_to_text(filename, UPLOAD_FOLDER)
    else:
        convert_doc_to_text(filename, UPLOAD_FOLDER)
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
        print "Erroring in reading file" # TODO ERROR
    # Delete the files and return the string of words
    os.system('rm -f ' + new_filename)
    os.system('rm -f ' + UPLOAD_FOLDER + filename)
    return data


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def split_text(data, DISALLOWED_WORD_LIST):
    data = data.replace('\t', '')
    data_list = data.split(' ')
    clean_list = []
    for word in data_list:
        if not word.startswith("/"):
            for dwl in DISALLOWED_WORD_LIST:
                word = word.replace(dwl, '')
            word = word.decode('utf-8', 'ignore')
            clean_list.append(word)
        clean_list_set = set(clean_list)
        clean_list_set_list = list(clean_list_set)
    return clean_list_set_list


def get_uncommon_words(data_list, FREQUENCY_LIMIT):
    data_list_freq = {}
    wordApi = WordApi.WordApi(client)
    for word in data_list:
        try:
            freq = wordApi.getWordFrequency(word)
            if freq.totalCount <= FREQUENCY_LIMIT and freq.totalCount > 0:
                data_list_freq[word] = freq.totalCount
        except urllib2.HTTPError as e:
            pass  # When the word doesn't exist, it throws a HTTP Error
    return data_list_freq


def get_definitions(data_list_freq):
    data_list_def = {}
    wordApi = WordApi.WordApi(client)
    for word in data_list_freq.keys():
        try:
            word = word.decode('ascii', 'ignore')
            defin = wordApi.getDefinitions(word)
            if (defin is not None):
                if (len(defin) > 0):
                    data_list_def[word] = defin[0].text
        except Exception as e:
            pass  # TODO log ERROR
    return data_list_def


def get_random_defintions(length):
    total_count = length * NUM_OF_RANDOM_DEF
    random_defintions = []
    wordsApi = WordsApi.WordsApi(client)
    wordApi = WordApi.WordApi(client)
    for x in range(total_count):
        example = wordsApi.getRandomWord(hasDictionaryDef=True,
                                         minDictionaryCount=2)
        exampleDef = wordApi.getDefinitions(example.word)
        random_defintions.append(exampleDef[0].text)
    return random_defintions


def make_questions(data_list_def, list_random_def):
    questions = {}
    count = 0
    definitions = []
    for word in data_list_def:
        for x in range(NUM_OF_RANDOM_DEF):
            definitions.append(list_random_def[count])
            count = count + 1
        definitions.append(data_list_def[word])
        random.shuffle(definitions)
        questions[word] = definitions
        definitions = []
    return questions
