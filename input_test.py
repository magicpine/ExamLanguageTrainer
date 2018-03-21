import os


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
    #print (example) # str
    example  = example.replace('\t', '')
    exampleList = example.split(' ')
    cleanList = []
    for word in exampleList:
        if word.startswith("\\"):
            print(word)
            cleanList.append(word)
    print(exampleList)
