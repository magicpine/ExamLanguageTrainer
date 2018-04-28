# Used for file formats
import time


def log_HTTP_Error(ip, message, mongo):
    ''' Logs HTTP ERRORS '''
    http_message = {'TIME': time.strftime('%Y%m%d%H%M'), 'IP': ip, 'MESSAGE': message}
    mongo.db.http.insert_one(http_message).inserted_id


def log_API_error(message, mongo):
    ''' Logs API ERRORS '''
    api_message = {'TIME': time.strftime('%Y%m%d%H%M'), 'MESSAGE': message}
    mongo.db.api.insert_one(api_message).inserted_id


def log_info(total_words, total_uncommon_words, total_uncommon_def, mongo):
    ''' Logs Word gathering info '''
    info = ('MESSAGE: ' + 'Total Words Collected: ' + str(total_words) +
            ' Total Uncommon Words found: ' + str(total_uncommon_words) +
            ' Total Uncommon words found with definitions: ' +
            str(total_uncommon_def))
    log_message = {'TIME': time.strftime('%Y%m%d%H%M'), 'MESSAGE': info}
    mongo.db.logs.insert_one(log_message).inserted_id


def get_code(words):
    ''' Generates the code based on the words
        returns the generated code '''
    total_length = len(words)
    words_keys = words.keys()
    fwfl = words_keys[0][0]
    fwll = words_keys[0][-1]
    lwfl = words_keys[-1][0]
    lwll = words_keys[-1][-1]
    ascii_value = 0
    for word in words_keys:
        ascii_value = ascii_value + ord(word[0])
    return str(total_length) + fwfl + fwll + lwfl + lwll + str(ascii_value)
