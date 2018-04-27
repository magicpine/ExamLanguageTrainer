# Used for file formats
import time
# Used to write files in UTF-8
import codecs


# File locations
LOGS_FOLDER = 'logs/'
ERROR_FOLDER = 'errors/'


def log_HTTP_Error(ip, message):
    ''' Logs HTTP ERRORS '''
    err = 'IP: ' + ip + ' MESSAGE: ' + message + '\n'
    filename = ERROR_FOLDER + 'http_' + time.strftime('%Y%m%d') + '.err'
    with open(filename, 'a') as myfile:
        myfile.write('TIME: ' + time.strftime('%H%M') + ' ' + err)


def log_file_error(message):
    ''' Logs FILE ERRORS '''
    err = 'MESSAGE: ' + message + '\n'
    filename = ERROR_FOLDER + 'file_' + time.strftime('%Y%m%d') + '.err'
    with open(filename, 'a') as myfile:
        myfile.write('TIME: ' + time.strftime('%H%M') + ' ' + err)


def log_API_error(message):
    ''' Logs API ERRORS '''
    err = 'MESSAGE: ' + message + '\n'
    filename = ERROR_FOLDER + 'api_' + time.strftime('%Y%m%d') + '.err'
    with codecs.open(filename, 'a', 'utf-8') as myfile:
        myfile.write('TIME: ' + time.strftime('%H%M') + ' ' + err)


def log_information(total_words, total_uncommon_words, total_uncommon_def):
    ''' Logs Word gathering info '''
    info = 'MESSAGE: ' + 'Total Words Collected: ' + str(total_words) + ' Total Uncommon Words found: ' + str(total_uncommon_words) + ' Total Uncommon words found with defintions: ' + str(total_uncommon_def) + '\n'
    filename = LOGS_FOLDER + 'words_' + time.strftime('%Y%m%d') + '.log'
    with codecs.open(filename, 'a', 'utf-8') as myfile:
        myfile.write('TIME: ' + time.strftime('%H%M') + ' ' + info)
