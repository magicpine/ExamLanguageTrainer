import os


def getText(filename):
    sys = 'soffice --headless --convert-to txt:Text ' + filename
    os.system(sys)
    new_filename = filename.split('.')[0] + '.txt'
    print (new_filename)
    with open(new_filename, 'r') as myfile:
        data=myfile.read().replace('\n', '')
    return data

if '__main__' == __name__:
    example = getText('ass3-2018.doc')
    print (example) # str
    example  = example.replace('\t', '')
    
    exampleList = example.split(' ')
    print(exampleList)
