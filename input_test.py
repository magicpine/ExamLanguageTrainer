import os

DISALLOWED_WORD_LIST = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',',
                        '\t', ':', '.', '(', ')', '?', '"', "'",'-',';','\\x')

def getText(filename):
    sys = 'soffice --headless --convert-to txt:Text ' + filename
    os.system(sys)
    new_filename = filename.split('.')[0] + '.txt'
    #print (new_filename)
    with open(new_filename, 'r') as myfile:
        data=myfile.read().replace('\n', '')
    return data

if '__main__' == __name__:
    example = getText('tmp/ass3-2018.doc')
    example = example.decode('utf-8', 'ignore')
    #print (example) # str
    #example  = example.replace('\t', '')
    exampleList = example.split(' ')
    cleanList = []
    for word in exampleList:
        #escape .docx and .doc special characters that start with '/'
        if not word.startswith("/"):
            for dwl in DISALLOWED_WORD_LIST:
                word = word.replace(dwl, '')
            print(word)
            cleanList.append(word)
    cleanlistset = set(cleanList)
    cleanlistsetlist = list(cleanlistset)
    print(cleanlistsetlist)
