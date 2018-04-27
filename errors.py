# Used for file formats
import time
# Used to write files in UTF-8
import codecs

# Variables
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
