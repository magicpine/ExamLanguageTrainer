# Used to convert files to Text
import os
# Used for HTTPError
import urllib2
# Used to shuffle definitions
import random
# Used to use the api
from wordnik import *


apiUrl = 'http://api.wordnik.com/v4'
apiKey = '972e0b90c32a7859fc4944c19a603e0a6cf53a45963d7ee42 '
client = swagger.ApiClient(apiKey, apiUrl)


NUM_OF_RANDOM_DEF = 3


def get_text(filename, UPLOAD_FOLDER):
    print sys
    os.system(sys)
    sys = 'soffice --headless --convert-to txt:Text '+UPLOAD_FOLDER+filename
    new_filename = filename.split('.')[0] + '.txt'
    print new_filename
    with open(new_filename, 'r') as myfile:
        data = myfile.read().replace('\n', '')
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
            example = wordApi.getWordFrequency(word)
            if example.totalCount <= FREQUENCY_LIMIT and
            example.totalCount > 0:
                data_list_freq[word] = example.totalCount
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
