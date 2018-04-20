#Used to run the webapp
from flask import (Flask, render_template, request, session, redirect, url_for, Markup, flash)
#Used to save files
from werkzeug.utils import secure_filename
#This is the functions
from words import *


FREQUENCY_LIMIT = 100
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'doc', 'docx'])
DISALLOWED_WORD_LIST = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',',
                        '\t', ':', '.', '(', ')', '?', '"', "'",'-',';',)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'itsmybirthdaythatsthepassword'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/review', methods=["POST"])
def review():
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
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = get_text(filename, UPLOAD_FOLDER)
        data_list = split_text(data, DISALLOWED_WORD_LIST)
        data_list_freq = get_uncommon_words(data_list, FREQUENCY_LIMIT)
        data_list_def = get_definitions(data_list_freq)
        session['defintions'] = data_list_def
        return render_template('review.html', words=data_list_def)


@app.route('/update', methods=["POST"])
def update():
    old_data_list_def = session['defintions']
    data_list_def = {}
    for word in old_data_list_def:
        if request.form.get(word):
            data_list_def[word] = old_data_list_def[word]
    session['defintions'] = data_list_def
    print data_list_def
    return redirect(url_for('quiz'), code=307) #code for POST


@app.route('/quiz', methods=["POST"])
def quiz():
    data_list_def = session['defintions']
    list_random_def = get_random_defintions(len(data_list_def))
    questions = make_questions(data_list_def, list_random_def)
    return render_template('quiz.html', words=questions)


@app.route('/answers', methods=["POST"])
def answers():
    correct = []
    wrong = {}
    data_list_def = session['defintions']
    for word in data_list_def:
        answered = request.form.get(word)
        if data_list_def[word] == answered:
            correct.append(word)
        else:
            wrong[word] = data_list_def[word]
    return render_template('answers.html', correct = correct, wrong = wrong,
                           correct_total=len(correct), total=len(data_list_def))


if __name__ == '__main__':
    app.secret_key = 'itsmybirthdaythatsthepassword'
    app.run(debug=True)
