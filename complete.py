from init import queries
from AutoCompleteData import AutoCompleteData
from string import ascii_lowercase
from init import file_list
import os
import linecache


def replace(sub_text, index):
    for char in ascii_lowercase:
        new_str = sub_text[:index] + char + sub_text[index + 1:]
        if new_str in queries.keys():
            return queries[new_str]
    return set()


def add(sub_text, index):
    for char in ascii_lowercase:
        new_str = sub_text[:index] + char + sub_text[index:]
        if new_str in queries.keys():
            return queries[new_str]
    return set()


def sub(sub_text, index):
    for char in ascii_lowercase:
        new_str = sub_text[:index] + sub_text[index + 1:]
        if new_str in queries.keys():
            return queries[new_str]
    return set()


def create_auto_complete_data(list_of_indexes):
    auto_complete_data_list = []
    for i,index in enumerate(list_of_indexes):
        # my_file = open(file_list[index].file_name)
        # sentences = my_file.read().split("\n")
        sentences = " ".join(linecache.getline(file_list[index].file_name,file_list[index].offset).split("\n"))
        sentences = sentences[:len(sentences)-1]
        auto_complete_data_list.append(
            AutoCompleteData(sentences, os.path.basename(file_list[index].file_name),
                             file_list[index].offset, 0))
    return auto_complete_data_list


def complete(sub_text):
    score_list = [len(sub_text)*2]*5
    if sub_text in queries.keys():
        return create_auto_complete_data(queries[sub_text])
    res = []
    for index in range(3, len(sub_text)):
        res += (replace(sub_text, index))
        if len(res) > 5: return create_auto_complete_data(res[:5])
    for index in range(3, len(sub_text)):
        res += (add(sub_text, index))
        if len(res) > 5: return create_auto_complete_data(res[:5])
        res+= (sub(sub_text, index))
        if len(res) > 5: return create_auto_complete_data(res[:5])
    if len(sub_text) > 2:
        res += (replace(sub_text, 2))
        if len(res) > 5: return create_auto_complete_data(res[:5])
    if len(sub_text) > 1:
        res +=((replace(sub_text, 1)))
        if len(res) > 5: return create_auto_complete_data(res[:5])
    if len(sub_text) > 3:
        res +=(add(sub_text, 3))
        if len(res) > 5: return create_auto_complete_data(res[:5])
        res += (sub(sub_text, 3))
        if len(res) > 5: return create_auto_complete_data(res[:5])
    res +=(replace(sub_text, 0))
    if len(res) > 5: return create_auto_complete_data(res[:5])
    for index in range(0, 2)[::-1]:
        res += (add(sub_text, index))
        if len(res) > 5: return create_auto_complete_data(res[:5])
        res +=(sub(sub_text, index))
        if len(res) > 5: return create_auto_complete_data(res[:5])
    return create_auto_complete_data(res)
