import os
import zipfile
from AutoCompleteData import AutoCompleteData
queries = {}


def update_five_words(sentence, text_file, list_of_sentence, score):
    if len(list_of_sentence) < 5:
        list_of_sentence.append(AutoCompleteData(sentence, text_file, 0, score))
        return


def find_score(sub_word):
    return len(sub_word) * 2


def read_data(file_name):
    my_file = open(file_name)
    data = my_file.read().split("\n")
    for sentence in data:
        sub_words = set([sentence[i:j].lower() for i in range(len(sentence)) for j in range(i + 1, len(sentence) + 1)])
        for sub_word in sub_words:
            score_sentence = find_score(sub_word)
            if sub_word not in queries.keys():
                queries[sub_word] = []
            update_five_words(sentence, file_name, queries[sub_word], score_sentence)


def directories_traversal(directory_, counter=0):
    entries = os.listdir(directory_)
    counter+=1
    for entry in entries:
        if os.path.isdir(directory_ + '/' + entry):
            print(entry)
            directories_traversal(directory_ + '/' + entry)
        else:
            print(entry)
            read_data(directory_ + '/' + entry)


def init_dict():
    # data_zip = zipfile.ZipFile('technology_texts.zip', 'r')
    # data_zip.extractall(path='extract_dir/')
    # directories_traversal('extract_dir/')
    read_data("license.txt")