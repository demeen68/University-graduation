import pickle


def save_stop_words_list():
    stopwords = open(
        'stopwords.txt')
    stopwords = list(stopwords)
    stword = []
    for words in stopwords:
        stword.append(words.replace('\t', '').replace('\n', ''))
    output = open('stopwords.pkl', 'wb')
    pickle.dump(stword, output)
    output.close()


def read_stop_words_list():
    motion_dic = pickle.load(open('stopwords.pkl', 'rb'))
