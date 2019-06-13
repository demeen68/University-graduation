import pickle


# Save motion.txt as motion_dic.pkl
def save_motion_txt():
    motion_words = open('motion.txt')
    motion_words = list(motion_words)
    motion_compare = {}
    for motion_list in motion_words:
        motion_list = motion_list.split(',')
        motion_compare.setdefault(motion_list[0], []).append(motion_list[1])
        motion_compare.setdefault(motion_list[0], []).append(motion_list[2])

    output = open('motion_dic.pkl', 'wb')
    pickle.dump(motion_compare, output)
    output.close()


def get_motion_txt():
    content_s = ['瑞雪', '瑞雪', '分享', '自恃']
    motion_dic = pickle.load(open('motion_dic.pkl', 'rb'))
    main_motion = {}
    for words in content_s:
        motion_list = motion_dic.get(words, '')
        if motion_list:
            # check if we have gotton this motion
            if main_motion.get(motion_list[0]):
                main_motion[motion_list[0]] += float(motion_list[1])
            else:
                main_motion.update({motion_list[0]: float(motion_list[1])})
