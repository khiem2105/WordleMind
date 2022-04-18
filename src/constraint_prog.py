import os

import random
from copy import deepcopy

from itertools import combinations
from collections import Counter


def get_words(file="dico.txt"):
    words = []
    file_path = os.getcwd() + "/data/" + file
    with open(file_path, "r") as f:
        for line in f.readlines():
            words.append(line[:-1])

    return words

def get_secret_word(words, n):
    words_n = [w for w in words if len(w) == n]
    return words_n[random.randint(0, len(words_n)-1)]


def generate_letter_list(word):
    return [(word[i], i) for i in range(len(word))]

def generate_frequency_list(word):
    return dict(Counter(word))

def check_occurence(wrong_letters_occurence, right_letters_occurence, occurence_list):
    for l, o in wrong_letters_occurence.items():
        if l in right_letters_occurence:
            if o + right_letters_occurence[l] != occurence_list[l]:
                return False
        else:
            if o != occurence_list[l]:
                return False

    return True

def compare_string(word, secret_word):
    right, wrong = 0, 0
    
    for i in range(len(word)):
        if word[i] == secret_word[i]:
            right += 1
        elif word[i] in secret_word:
            wrong += 1

    return right, wrong


def generate_constraint(word, right, wrong):
    index_list = generate_letter_list(word)
    occurence_list = generate_frequency_list(word)

    constraints = []
    for right_assigns in combinations(index_list, right):        
        right_letters = [a[0] for a in right_assigns]
        right_letters_occurence = generate_frequency_list(right_letters)

        left_index = [index for index in index_list if index not in right_assigns]
        left_letters = [i[0] for i in left_index]

        for wrong_assigns in combinations(left_index, wrong):
            constraint = dict()
            constraint["right"] = list(right_assigns)
            wrong_letters = [a[0] for a in wrong_assigns]
            wrong_letters_occurence = generate_frequency_list(wrong_letters)

            intersections = set(left_letters).intersection(set(right_letters))

            if not intersections.issubset(wrong_letters):
                continue
            
            if not check_occurence(wrong_letters_occurence, right_letters_occurence, occurence_list):
                continue
            
            
            constraint["wrong"] = list(wrong_assigns)
            # constraint["not_in"] = tuple((i, c) for i,c in index_list if (i, c) not in wrong_assigns and (i,c) not in right_assigns and 
            #                             i not in right_letters and i not in wrong_letters)
            constraint["not_in"] = list(set(i for i, c in index_list if (i, c) not in wrong_assigns and (i,c) not in right_assigns and 
                                        i not in right_letters and i not in wrong_letters))

            constraints.append(constraint)



    return constraints


def build_word_from_instanciation(instanciation):
    return "".join(instanciation.values())

def check_wrong_index(wrong_assigns, word):
    for wrong_assign in wrong_assigns:
        indices_in_word = [i for i, c in enumerate(word) if c == wrong_assign[0]]
        if len(indices_in_word) == 0 or (wrong_assign[1] in indices_in_word and len(indices_in_word) == 1):
            return False 

    return True

def check_compatible_words(word1, word2, right, wrong):
    constraints = generate_constraint(word2, right, wrong)
    letter_list = generate_letter_list(word1)
    for constraint in constraints:
        right_assigns = constraint["right"]
        wrong_assigns = constraint["wrong"]
        not_in = constraint["not_in"]

        if set(right_assigns).issubset(letter_list) and check_wrong_index(wrong_assigns, word1) and all(c not in word1 for c in not_in):
            return True

    return False

def check_compatible(instanciation, words, proposed_words, secret_word, domains):
    valid_words_from_instanciation = [w for w in words if w[:max(instanciation.keys()) + 1] == build_word_from_instanciation(instanciation) and len(w) == len(secret_word)]
    # print(valid_words_from_instanciation)

    compatible_words = []
    new_domains = deepcopy(domains)

    for w in valid_words_from_instanciation:
        # print(f"word: {w}")
        is_compatible = True
        for proposed_w in proposed_words:
            # print(f"proposed word: {proposed_w}, secret_word: {secret_word}")
            right, wrong = compare_string(proposed_w, secret_word)
            # print(f"right: {right}, wrong: {wrong}")
            if not check_compatible_words(w, proposed_w, right, wrong):
                is_compatible = False
                break
        
        # print(f"{w} is compatible: {is_compatible}")
        if is_compatible:
            compatible_words.append(w)

    # print(compatible_words)

    if len(compatible_words) == 0:
        return False, new_domains
    else:
        for i in range(max(instanciation.keys())+1, len(domains)):
            new_domains[i] = list(set(w[i] for w in compatible_words))

        return True, new_domains

def backtracking(words, secret_word, proposed_words, V, domains, instanciation={}):
    if len(V) == 0:
        return build_word_from_instanciation(instanciation)
    
    next = V[0]
    for value in domains[next]:
        instanciation[next] = value
        # print(instanciation)
        is_compatible, new_domains = check_compatible(instanciation, words, proposed_words, secret_word, domains)
        if is_compatible:
            result = backtracking(words, secret_word, proposed_words, V[1:], new_domains, deepcopy(instanciation))
            if result is not False and result in words and result not in proposed_words:
                # print(result)
                compatible = True
                for proposed_w in proposed_words:
                    right, wrong = compare_string(proposed_w, secret_word)
                    if not check_compatible_words(result, proposed_w, right, wrong):
                        compatible = False
                        break
                if compatible:            
                    return result

    return False

def solve_worlde(secret_word, words, verbose=True):
    n = len(secret_word)

    V = [i for i in range(n)]
    domains = [[chr(i) for i in range(97, 123)] for _ in range(n)]

    n_try = 1
    proposed_words = []

    next = backtracking(words, secret_word, proposed_words, V, domains)
    if verbose:
        print(f"Try {n_try}: {next}")
    while next != secret_word:
        proposed_words.append(next)
        next = backtracking(words, secret_word, proposed_words, V, domains)
        n_try += 1
        if verbose:
            print(f"Try {n_try}: {next}")

    return n_try