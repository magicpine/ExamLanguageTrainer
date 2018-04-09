#Used to run the webapp
from flask import (Flask, render_template, request, session,
                   redirect, url_for, Markup, flash)
#Used to convert files to Text
import os
#Used to shuffle definitions
import random
#Used for HTTPError
import urllib2
#Used to save files
from werkzeug.utils import secure_filename
#Used to use the api
from wordnik import *
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '972e0b90c32a7859fc4944c19a603e0a6cf53a45963d7ee42 '
client = swagger.ApiClient(apiKey, apiUrl)

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'doc', 'docx'])
DISALLOWED_WORD_LIST = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',',
                        '\t', ':', '.', '(', ')', '?', '"', "'",'-',';',)
FREQUENCY_LIMIT = 100

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'itsmybirthdaythatsthepassword'


def get_text(filename):
    sys = 'soffice --headless --convert-to txt:Text ' + UPLOAD_FOLDER + filename
    print sys
    os.system(sys)
    new_filename = filename.split('.')[0] + '.txt'
    print new_filename
    with open(new_filename, 'r') as myfile:
        data=myfile.read().replace('\n', '')
    os.system('rm -f ' + new_filename)
    os.system('rm -f ' + UPLOAD_FOLDER + filename)
    return data


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def split_text(data):
    data  = data.replace('\t', '')
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


def get_freq(data_list):
    data_list_freq = {}
    wordApi = WordApi.WordApi(client)
    for word in data_list:
        try:
            example = wordApi.getWordFrequency(word)
            data_list_freq[word] = example.totalCount
        except urllib2.HTTPError as e:
            pass
    return data_list_freq


def get_uncommon_words(data_list_freq):
    data_list_freq_new = {}
    for word, freq in data_list_freq.iteritems():
        if freq <= 100 and freq > 0:
            data_list_freq_new[word] = freq
    return data_list_freq_new


def get_definitions(data_list_freq):
    data_list_def = {}
    wordApi = WordApi.WordApi(client)
    for word in data_list_freq.keys():
        word = word.decode('ascii', 'ignore')
        defin = wordApi.getDefinitions(word)
        if (defin != None):
            if (len(defin) > 0):
                data_list_def[word] = defin[0].text
    return data_list_def


def get_random_defintions(length):
    total_count = length * 3
    random_defintions = []
    wordsApi = WordsApi.WordsApi(client)
    wordApi = WordApi.WordApi(client)
    for x in range(total_count):
        example = wordsApi.getRandomWord(hasDictionaryDef='True',minDictionaryCount=2)
        exampleDef = wordApi.getDefinitions(example.word)
        random_defintions.append(exampleDef[0].text)
    return random_defintions


def make_questions(data_list_def, list_random_def):
    questions = {}
    count = 0
    definitions = []
    for word in data_list_def:
        for x in range(3):
            definitions.append(list_random_def[count])
            count = count + 1
        definitions.append(data_list_def[word])
        random.shuffle(definitions)
        questions[word] = definitions
        definitions = []
    return questions


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/quiz', methods=["POST"])
def quiz():
    # check if the post request has the file part
    if 'exam' not in request.files:
        flash('No file part')
        return 'NO FILE' #TODO ERROR
    file = request.files['exam']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return 'No selected file' #TODO ERROR
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = get_text(file.filename)
        data_list = split_text(data)
        data_list_freq = get_freq(data_list)
        data_list_freq = get_uncommon_words(data_list_freq)
        data_list_def = get_definitions(data_list_freq)
        session['correct_defintions'] = data_list_def
        list_random_def = get_random_defintions(len(data_list_freq))
        questions = make_questions(data_list_def, list_random_def)
        return render_template('quiz.html',
                               words=questions)


@app.route('/answers', methods=["POST"])
def answers():
    correct = []
    wrong = {}
    data_list_def = session['correct_defintions']
    for word in data_list_def:
        answered = request.form[word]
        if data_list_def[word] == answered:
            correct.append(word)
        else:
            wrong[word] = data_list_def[word]
    return render_template('answers.html', correct = correct, wrong = wrong,
                           correct_total=len(correct), total=len(data_list_def))


if __name__ == '__main__':
    app.run(debug=True)
