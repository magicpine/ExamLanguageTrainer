# Used to run the webapp
from flask import (Flask, render_template, request, session, redirect,
                   url_for, Markup, flash)
# Used to save files
from werkzeug.utils import secure_filename
# This is the functions
from words import *
# This is used to save the tests
from codes import *
# This is used for logging information
from log_errors_info import *

# FILE LOCATIONS
UPLOAD_FOLDER = 'uploads/'
TESTS_FOLDER = 'tests/'


# Logging and error messages
FILE_UPLOAD_ERROR_NONE = 'No file exists'
FILE_UPLOAD_ERROR_EXTENTIONS = 'Wrong file extentions used'
NO_CODE = 'Please enter in a code'
WRONG_CODE = 'Wrong code entered'
API_ERROR = 'The API has stopped responding. Please try again'


# Variables
FREQUENCY_LIMIT = 100
ALLOWED_EXTENSIONS = set(['txt', 'doc', 'docx', 'obt', 'rtf',
                          'pdf', 'ppt', 'pptx'])
DISALLOWED_WORD_LIST = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',',
                        '\t', ':', '.', '(', ')', '?', '"', "'", '-', ';',)


# Used for FLASK
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'itsmybirthdaythatsthepassword'


@app.route('/')
def index():
    ''' Home Page '''
    return render_template('index.html')


@app.route('/review', methods=["POST"])
def review():
    ''' Breaks down the file into uncommon words and defintions
        Brings you to a REVIEW page for the words you wanna keep.'''
    # check if the post request has the file part
    if 'exam' not in request.files:
        log_HTTP_Error(request.remote_addr, FILE_UPLOAD_ERROR_NONE)
        flash(FILE_UPLOAD_ERROR_NONE)
        return redirect(url_for('index'))
    # get the file and check to see if its valid
    file = request.files['exam']
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = get_text(filename, UPLOAD_FOLDER)
        # The function will return ERROR if it fails
        if data == 'ERROR':
            flash('Server could not read the file')
            return redirect(url_for('index'))
        data_list = split_text(data, DISALLOWED_WORD_LIST)
        data_list_freq = get_uncommon_words(data_list, FREQUENCY_LIMIT)
        if data_list_freq is None:
            flash(API_ERROR)
            return redirect(url_for('index'))
        data_list_def = get_definitions(data_list_freq)
        log_info(len(data_list), len(data_list_freq), len(data_list_def))
        session['defintions'] = data_list_def
        return render_template('review.html', words=data_list_def)
    # File is not a valid file
    log_HTTP_Error(request.remote_addr, FILE_UPLOAD_ERROR_EXTENTIONS)
    flash(FILE_UPLOAD_ERROR_EXTENTIONS)
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    test_code = request.form.get('test')
    if test_code.strip() == '':
        flash(NO_CODE)
        return redirect(url_for('index'))
    return redirect(url_for('quiz', code=test_code), code=307)  # code for POST


@app.route('/update', methods=["POST"])
def update():
    ''' Takes the words after review and stores the words '''
    old_data_list_def = session['defintions']
    data_list_def = {}
    for word in old_data_list_def:
        if request.form.get(word):
            data_list_def[word] = old_data_list_def[word]
    code = save_test_file(data_list_def, TESTS_FOLDER)
    quiz_code = 'quiz?code=' + code
    return render_template('saved.html', code=code, quiz_code=quiz_code)


@app.route('/quiz', methods=["POST"])
def quiz():
    ''' Takes the words and displays the test '''
    code = request.args.get('code')
    data_list_def = load_test_file(code, TESTS_FOLDER)
    if data_list_def is None:
        flash(WRONG_CODE)
        return redirect(url_for('index'))
    list_random_def = get_random_defintions(len(data_list_def))
    questions = make_questions(data_list_def, list_random_def)
    answer_code = 'answers?code=' + code
    return render_template('quiz.html', words=questions,
                           answer_code=answer_code)


@app.route('/answers', methods=["POST"])
def answers():
    ''' Tallys up the answers from the test & displays what you got right '''
    correct = []
    wrong = {}
    code = request.args.get('code')
    data_list_def = load_test_file(code, TESTS_FOLDER)
    for word in data_list_def:
        answered = request.form.get(word)
        if data_list_def[word] == answered:
            correct.append(word)
        else:
            wrong[word] = data_list_def[word]
    return render_template('answers.html', correct=correct, wrong=wrong,
                           correct_total=len(correct),
                           total=len(data_list_def))

# Only used for local use
if __name__ == '__main__':
    app.secret_key = 'itsmybirthdaythatsthepassword'
    app.run(debug=True)
