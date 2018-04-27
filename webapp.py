# Used to run the webapp
from flask import (Flask, render_template, request, session, redirect,
                   url_for, Markup, flash)
# Used to save files
from werkzeug.utils import secure_filename
# This is the functions
from words import *
# This is used to log errors
from errors import *

# Variables
FREQUENCY_LIMIT = 100
UPLOAD_FOLDER = 'uploads/'
FILE_UPLOAD_ERROR_NONE = 'No file exists'
FILE_UPLOAD_ERROR_EXTENTIONS = 'Wrong file extentions used'
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
        data_list_def = get_definitions(data_list_freq)
        session['defintions'] = data_list_def
        return render_template('review.html', words=data_list_def)
    # File is not a valid file
    log_HTTP_Error(request.remote_addr, FILE_UPLOAD_ERROR_EXTENTIONS)
    flash(FILE_UPLOAD_ERROR_EXTENTIONS)
    return render_template('index.html')


@app.route('/update', methods=["POST"])
def update():
    ''' Takes the words after review and stores the words '''
    old_data_list_def = session['defintions']
    data_list_def = {}
    for word in old_data_list_def:
        if request.form.get(word):
            data_list_def[word] = old_data_list_def[word]
    session['defintions'] = data_list_def
    return redirect(url_for('quiz'), code=307)  # code for POST


@app.route('/quiz', methods=["POST"])
def quiz():
    ''' Takes the words and displays the test '''
    data_list_def = session['defintions']
    list_random_def = get_random_defintions(len(data_list_def))
    questions = make_questions(data_list_def, list_random_def)
    return render_template('quiz.html', words=questions)


@app.route('/answers', methods=["POST"])
def answers():
    ''' Tallys up the answers from the test & displays what you got right '''
    correct = []
    wrong = {}
    data_list_def = session['defintions']
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
