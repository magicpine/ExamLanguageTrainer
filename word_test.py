from wordnik import *
apiUrl = 'http://api.wordnik.com/v4'
apiKey = '972e0b90c32a7859fc4944c19a603e0a6cf53a45963d7ee42 '
client = swagger.ApiClient(apiKey, apiUrl)

wordsApi = WordsApi.WordsApi(client)
example = wordsApi.getRandomWord(hasDictionaryDef='True',minDictionaryCount=2)
print(example.word) # str
wordApi = WordApi.WordApi(client)
exampleDef = wordApi.getDefinitions(example.word)
for tmp in exampleDef:
    print (tmp.text) # str
example = wordApi.getWordFrequency(example.word)
print (example.totalCount) #int
