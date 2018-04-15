#Used to run the webapp
from flask import (Flask, render_template, request, session,redirect, url_for, Markup, flash)
#Used to save files
from werkzeug.utils import secure_filename
#This is the functions
from words import *


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'doc', 'docx'])
DISALLOWED_WORD_LIST = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',',
                        '\t', ':', '.', '(', ')', '?', '"', "'",'-',';',)
FREQUENCY_LIMIT = 100

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'itsmybirthdaythatsthepassword'


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
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data = get_text(filename, UPLOAD_FOLDER)
        data_list = split_text(data, DISALLOWED_WORD_LIST)
        data_list_freq = get_freq(data_list)
        data_list_freq = get_uncommon_words(data_list_freq, FREQUENCY_LIMIT)
        #TODO Cut this in half for review of words.
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
