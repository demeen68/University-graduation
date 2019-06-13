import pickle


def create_baidu_ignore():
    ignore_words = open(
        'baidu_ignore.txt')
    ignore_words = list(ignore_words)
    ig_word = []
    for words in ignore_words:
        ig_word.append(words.replace('\t', '').replace('\n', ''))
    output = open('baidu_ignore.pkl', 'wb')
    pickle.dump(ig_word, output)
    output.close()
