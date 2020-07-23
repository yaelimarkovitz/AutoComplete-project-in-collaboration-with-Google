from init import queries
from AutoCompleteData import AutoCompleteData
from string import ascii_lowercase
from init import file_dict
import os
import linecache
import pandas as pd


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


def create_auto_complete_data(list_of_indexes, score_list):
    auto_complete_data_list = []
    for i, index in enumerate(list_of_indexes):
        sentences = " ".join(linecache.getline(file_dict[index].file_name, file_dict[index].offset).split("\n"))
        sentences = sentences[:len(sentences) - 1]
        auto_complete_data_list.append(
            AutoCompleteData(str(i + 1) + ". " + sentences.strip(), os.path.basename(file_dict[index].file_name),
                             file_dict[index].offset, score_list[i]))
    return auto_complete_data_list


def remove_duplications(res):
    pd.Series(res).drop_duplicates().tolist()


def try_to_fix(start_index, end_index, func_to_do, score_to_sub, sub_text, score_list):
    sub_text_len = len(sub_text)
    ret_res = []
    for index in range(start_index, end_index):
        ret_res += func_to_do(sub_text, index)
        score_list += [sub_text_len * 2 - score_to_sub] * len(ret_res)
        remove_duplications(ret_res)
        if len(ret_res) > 5: return ret_res[:5]
    return ret_res


def complete(sub_text):
    sub_tex_len = len(sub_text)
    score_list = []
    if sub_text in queries.keys():
        score_list += [sub_tex_len * 2] * 5
        return create_auto_complete_data(queries[sub_text], score_list)
    res = []
    res += try_to_fix(3, sub_tex_len, replace, 1, sub_text, score_list)
    if len(res) > 5: return create_auto_complete_data(res[:5], score_list)
    res += try_to_fix(4, sub_tex_len, add, 2, sub_text, score_list)
    if len(res) > 5: return create_auto_complete_data(res[:5], score_list)
    res += try_to_fix(4, sub_tex_len, sub, 2, sub_text, score_list)
    if len(res) > 5: return create_auto_complete_data(res[:5], score_list)
    if sub_tex_len > 2:
        res += try_to_fix(2, 3, replace, 3, sub_text, score_list)
        if len(res) > 5: return create_auto_complete_data(res[:5], score_list)
    if sub_tex_len > 1:
        res += try_to_fix(1, 2, replace, 4, sub_text, score_list)
        if len(res) > 5: return create_auto_complete_data(res[:5], score_list)
    if sub_tex_len > 3:
        res += try_to_fix(3, 4, add, 4, sub_text, score_list)
        if len(res) > 5: return create_auto_complete_data(res[:5], score_list)
        res += try_to_fix(3, 4, sub, 4, sub_text, score_list)
        if len(res) > 5: return create_auto_complete_data(res[:5], score_list)
    res += try_to_fix(0, 1, replace, 5, sub_text, score_list)
    if len(res) > 5: return create_auto_complete_data(res[:5], score_list)
    for index in range(0, 3)[::-1]:
        res += try_to_fix(index, index + 1, add, (((2 - index) * 2) + 6), sub_text, score_list)
        if len(res) > 5: return create_auto_complete_data(res[:5], score_list)
        res += try_to_fix(index, index + 1, sub, (((2 - index) * 2) + 6), sub_text, score_list)
        if len(res) > 5: return create_auto_complete_data(res[:5], score_list)
    return create_auto_complete_data(res, score_list)
