#!/usr/bin/python
# -*- coding: utf-8 -*-

# Used to run the webapp
from flask import (Flask, render_template, request, session, redirect,
                   url_for, Markup, flash, jsonify)
# Used to save files
from werkzeug.utils import secure_filename
# Used for the database
from flask_pymongo import PyMongo
# This is the functions
from words import *
# This is used for logging information
from log_errors_info import *


# FILE LOCATIONS
UPLOAD_FOLDER = 'uploads/'


# Logging and error messages
FILE_UPLOAD_ERROR_NONE = 'No file exists'
FILE_UPLOAD_ERROR_EXTENTIONS = 'Wrong file extensions used'
FILE_READ_ERROR = 'Server could not read the file'
NO_CODE = 'Please enter in a code'
WRONG_CODE = 'Wrong code entered'
API_ERROR = 'The API has stopped responding. Please try again'


# Variables
FREQUENCY_LIMIT = 100
ALLOWED_EXTENSIONS = set(['txt', 'doc', 'docx', 'obt', 'rtf',
                          'pdf', 'ppt', 'pptx'])
DISALLOWED_WORD_LIST = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',',
                        '\t', ':', '.', '(', ')', '?', '"', "'", '-', ';',
                        '/', '%', '$', '&', '‘', '€', '+', '*', '[', '’',
                        '_', '=', '”', '…', '“', '^', ']', '{', '}', '<',
                        '>', '~', '`', '|', '#', '@', '!', '•', '–', )


# Common Words list that is used to filter out most common words in files
FILTER_WORDS_FILE = 'filter_common_words.txt'
with open(FILTER_WORDS_FILE, 'r') as myfile:
    TOP_COMMON_WORDS_LIST = myfile.read().replace('\n', ' ').split(' ')


# Used for FLASK
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'itsmybirthdaythatsthepassword'


# Used for MongoDB
app.config['MONGO_DBNAME'] = 'elt'
mongo = PyMongo(app)


@app.route('/')
def index():
    ''' Home Page '''
    return render_template('index.html')


@app.route('/review', methods=["POST"])
def review():
    ''' Breaks down the file into uncommon words and definitions
        Brings you to a REVIEW page for the words you wanna keep.'''
    # check if the post request has the file part
    if 'exam' not in request.files:
        log_HTTP_Error(request.remote_addr, FILE_UPLOAD_ERROR_NONE, mongo)
        flash(FILE_UPLOAD_ERROR_NONE)
        return redirect(url_for('index'))
    # get the file and check to see if its valid
    file = request.files['exam']
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = get_text(filename, UPLOAD_FOLDER, mongo)
        # The function will return ERROR if it fails
        if data == 'ERROR':
            flash(FILE_READ_ERROR)
            return redirect(url_for('index'))
        data_list = split_text(data, DISALLOWED_WORD_LIST)
        # Take the list of words and filter it using a list of Common words
        data = [x for x in TOP_COMMON_WORDS_LIST if x not in data_list]
        data_list_freq = get_uncommon_words(data, FREQUENCY_LIMIT, mongo)
        if data_list_freq is None:
            flash(API_ERROR)
            return redirect(url_for('index'))
        data_list_def = get_definitions(data_list_freq, mongo)
        log_info(len(data), len(data_list_freq), len(data_list_def), mongo)
        session['definitions'] = data_list_def
        if len(data_list_def) == 0:
            return render_template('sorry.html')
        return render_template('review.html', words=data_list_def)
    # File is not a valid file
    log_HTTP_Error(request.remote_addr, FILE_UPLOAD_ERROR_EXTENTIONS, mongo)
    flash(FILE_UPLOAD_ERROR_EXTENTIONS)
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    ''' Takes the code from the index page and redirects you to the quiz'''
    test_code = request.form.get('test')
    if test_code.strip() == '':
        flash(NO_CODE)
        return redirect(url_for('index'))
    return redirect(url_for('quiz', code=test_code), code=307)  # code for POST


@app.route('/update', methods=["POST"])
def update():
    ''' Takes the words after review and stores the words '''
    old_data_list_def = session['definitions']
    data_list_def = {}
    for word in old_data_list_def:
        # Bootstrap labels don't uncheck after first click
        # So if the checkbox is checked that means they don't want the word
        if not request.form.get(word):
            data_list_def[word] = old_data_list_def[word]
    code = get_code(data_list_def)
    database_object = {'code': code, 'words': data_list_def}
    mongo.db.words.insert_one(database_object).inserted_id
    quiz_code = 'quiz?code=' + code
    return render_template('saved.html', code=code, quiz_code=quiz_code)


@app.route('/quiz', methods=["POST"])
def quiz():
    ''' Takes the words and displays the test '''
    code = request.args.get('code')
    data_list_def = list(mongo.db.words.find({'code': code}))
    if len(data_list_def) == 0:
        flash(WRONG_CODE)
        return redirect(url_for('index'))
    data_list_def = data_list_def[0]['words']
    list_random_def = get_random_defintions(len(data_list_def))
    questions = make_questions(data_list_def, list_random_def)
    answer_code = 'answers?code=' + code
    return render_template('quiz.html', words=questions,
                           answer_code=answer_code)


@app.route('/answers', methods=["POST"])
def answers():
    ''' Tallies up the answers from the test & displays what you got right '''
    correct = []
    wrong = {}
    code = request.args.get('code')
    data_list_def = list(mongo.db.words.find({'code': code}))
    if len(data_list_def) == 0:
        flash(WRONG_CODE)
        return redirect(url_for('index'))
    data_list_def = data_list_def[0]['words']
    for word in data_list_def:
        answered = request.form.get(word)
        if data_list_def[word] == answered:
            correct.append(word)
        else:
            wrong[word] = data_list_def[word]
    return render_template('answers.html', correct=correct, wrong=wrong,
                           correct_total=len(correct),
                           total=len(data_list_def))


@app.route('/faq')
def faq():
    ''' FAQ Page '''
    return render_template('faq.html')


# Only used for local use
if __name__ == '__main__':
    app.secret_key = 'itsmybirthdaythatsthepassword'
    app.run(debug=True)
