import os
import linecache
import zipfile
from AutoCompleteData import AutoCompleteData
from file_data import FileData
import re
import string

queries = {}
file_dict = {}


def read_from_file(index):
    # with open(file_list[index].file_name, encoding='utf-8') as cur_file:
    #     data = cur_file.read().split('\n')
    #     return data[file_list[index].offset]
    word = " ".join(linecache.getline(file_dict[index].file_name, file_dict[index].offset).split("\n"))
    return word


def clear_str(str):
    exclude = set(string.punctuation)
    str = ''.join(ch for ch in str if ch not in exclude)
    return str.lower()


def update_five_words(list_of_sentence, index, sub_word):
    if not list_of_sentence:
        list_of_sentence.append(index)
        return
    for i, sentence in enumerate(list_of_sentence):
        query = read_from_file(sentence)
        query = query.lower()
        if sub_word.lower() < query:
            list_of_sentence.insert(i, index)
            if (len(list_of_sentence)) > 5:
                list_of_sentence.pop()
            return
    if len(list_of_sentence) < 5:
        list_of_sentence.append(index)
        return


global_count = [0]


def read_data(file_name):
    counter = 0
    with open(file_name, encoding='utf-8') as my_file:
        data = my_file.read().split("\n")
    for sentence in data:
        counter += 1
        global_count[0] += 1
        file_dict[global_count[0]] = (FileData(file_name, counter))
        sub_words = set([sentence[i:j].lower() for i in range(len(sentence)) for j in range(i + 1, len(sentence) + 1)])
        for sub_word in sub_words:
            sub_word = clear_str(sub_word)
            if sub_word not in queries.keys():
                queries[sub_word] = []
            update_five_words(queries[sub_word], global_count[0], sentence)


def directories_traversal(directory_, counter=0):
    entries = os.listdir(directory_)
    counter += 1
    for entry in entries:
        if os.path.isdir(directory_ + '/' + entry):
            print(entry)
            directories_traversal(directory_ + '/' + entry)
        else:
            print(entry)
            read_data(directory_ + '/' + entry)


def init_dict():
    #data_zip = zipfile.ZipFile('technology_texts.zip', 'r')
    #data_zip.extractall(path='extract_dir/')
    #directories_traversal('extract_dir/')
     read_data("license.txt")
