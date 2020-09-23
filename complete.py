from init import queries
from model.AutoCompleteData import AutoCompleteData
from string import ascii_lowercase
from init import file_dict
import os
import linecache


def create_auto_complete_data(list_of_indexes, score_list):
    auto_complete_data_list = []
    for i, index in enumerate(list_of_indexes):
        sentences = " ".join(linecache.getline(file_dict[index].file_name, file_dict[index].offset).split("\n"))
        sentences = sentences[:len(sentences) - 1]
        auto_complete_data_list.append(
            AutoCompleteData(str(i + 1) + ". " + sentences.strip(), os.path.basename(file_dict[index].file_name),
                             file_dict[index].offset, score_list[i]))
    return auto_complete_data_list


def extract_string_from_file(file_name, line):
    return "".join(linecache.getline(file_name, (line)).split("\n"))


def score_of_replace(index):
    switcher = {
        0: -5,
        1: -4,
        2: -3,
        3: -2,
    }
    return switcher.get(index, -1)


def score_of_add_or_remove(index):
    switcher = {
        0: -10,
        1: -8,
        2: -6,
        3: -4,
    }
    return switcher.get(index, -2)


def get_score(input, index, flag):
    if flag:
        return len(input) * 2 + score_of_replace(index)
    return len(input) * 2 + score_of_add_or_remove(index)


def get_score(input, index, flag):
    if flag:
        return len(input) * 2 + score_of_replace(index)
    return len(input) * 2 + score_of_add_or_remove(index)


def update_match_k_best(matching_sentence, input, index, list_of_k_best, score_list, flag):
    current_score = get_score(input, index, flag)

    if matching_sentence in queries:
        if not list_of_k_best:
            for ind in range(len(queries[matching_sentence])):
                list_of_k_best.append(queries[matching_sentence][ind])
                score_list.append(current_score)

        for ind in range(len(queries[matching_sentence])):
            if current_score > min(score_list) and queries[matching_sentence][ind] not in list_of_k_best:
                list_of_k_best[score_list.index(min(score_list))] = queries[matching_sentence][ind]
                score_list[score_list.index(min(score_list))] = current_score


def complete(input):
    input_len = len(input)
    score_list = [input_len * 2] * 5

    if input in queries:
        return create_auto_complete_data(queries[input], score_list)
    list_of_k_best = []
    score_list = [0] * 5

    for i in range(len(input)):
        for ch in ascii_lowercase:
            replaced_sentence = input[:i] + ch + input[i + 1:]
            added_sentence = input[:i] + ch + input[i:]
            removed_sentence = input[:i] + ch + input[i + 1:]
            update_match_k_best(replaced_sentence, input, i, list_of_k_best, score_list, True)
            update_match_k_best(added_sentence, input, i, list_of_k_best, score_list, False)
            update_match_k_best(removed_sentence, input, i, list_of_k_best, score_list, False)

    return create_auto_complete_data(list_of_k_best, score_list)
