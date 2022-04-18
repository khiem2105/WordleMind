import numpy as np

import random

from constraint_prog import compare_string, check_compatible_words, get_secret_word

INFINITY = 10000

def distance(word1, word2):
    if len(word1) != len(word2):
        return INFINITY

    dist = 0
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            dist += 1

    return dist

def mutation(word, words, mut_rate=0.001):
    original_word = word
    list_w = list(word)
    for swapped in range(len(word)):
        if random.random() < mut_rate:
            swap_with = int(random.random() * len(word))

            c1 = list_w[swapped]
            c2 = list_w[swap_with]

            list_w[swapped] = c2
            list_w[swap_with] = c1

            word = "".join(list_w)

            if word not in words:
                word = min(words, key=lambda w: distance(word, w) if w != original_word else INFINITY) 

        return word

def evaluation(word, proposed_words, secret_word):
    not_compatible = 0

    for proposed_w in proposed_words:
        right, wrong = compare_string(proposed_w, secret_word)
        if not check_compatible_words(word, proposed_w, right, wrong):
            not_compatible += 1

    return not_compatible

def weight_fitness(population, proposed_words, secret_word):
    sum_fitness = sum(1 / (evaluation(individu, proposed_words, secret_word) + 1e-7) for individu in population)

    return [1 / (evaluation(individu, proposed_words, secret_word) + 1e-7) / sum_fitness for individu in population]

def selection(population, weighted_fitness):
    selected_index = np.random.choice(len(population), 2, p=weighted_fitness)

    return population[selected_index[0]], population[selected_index[1]]

def cross_over(parent1, parent2, words):
    l_parent1, l_parent2 = list(parent1), list(parent2)
    p = random.randint(0, len(parent1))
    child = l_parent1[:p]
    child = child + l_parent2[p:]

    child = "".join(child)
    if child not in words:
        child = min(words, key=lambda w: distance(child, w) if w != parent1 and w != parent2 else INFINITY)

    return child

def GA(words, secret_word, proposed_words, len_E=20, len_population=100, max_gen=100, mut_rate=0.001):
    E = []

    population = []
    # start with a random population
    while len(population) <= len_population:
        individu = get_secret_word(words, len(secret_word))
        if individu not in population:
            population.append(individu)

    for individu in population:
        if all(check_compatible_words(individu, proposed_w, *compare_string(proposed_w, secret_word)) for proposed_w in proposed_words):
            E.append(individu)
    n_gen = 0
    while n_gen < max_gen and len(E) <= len_E:
        if n_gen % 10 == 0:
            print("+")
        else:
            print(".")
        next_pop = []
        weighted_fitness = weight_fitness(population, proposed_words, secret_word)
        for _ in range(int(len_population / 2)):
            parent1, parent2 = selection(population, weighted_fitness)
            child1 = cross_over(parent1, parent2, words)
            child2 = cross_over(parent2, parent1, words)
            
            child1_mutated = mutation(child1, words, mut_rate=mut_rate)
            child2_mutated = mutation(child2, words, mut_rate=mut_rate)

            if all(check_compatible_words(child1_mutated, proposed_w, *compare_string(proposed_w, secret_word)) for proposed_w in proposed_words):
                E.append(child1_mutated)

            if all(check_compatible_words(child2_mutated, proposed_w, *compare_string(proposed_w, secret_word)) for proposed_w in proposed_words):
                E.append(child2_mutated)

            next_pop.append(child1_mutated)
            next_pop.append(child2_mutated)

        population = next_pop
        n_gen += 1

    return E

def solve_wordle_GA(words, secret_word, verbose=True):
    n_try = 1
    proposed_words = []

    E = GA(words, secret_word, proposed_words)
    print(E)
    if len(E) == 0:
        return 1
    next = E[random.randint(0, len(E)-1)]
    if verbose:
        print(f"Try {n_try}: {next}")
    while next != secret_word:
        proposed_words.append(next)
        E = GA(words, secret_word, proposed_words)
        if len(E) == 0:
            E = GA(words, secret_word, proposed_words)
        if len(E) == 0:
            return n_try
        n_try += 1
        next = E[random.randint(0, len(E)-1)]

        if verbose:
            print(f"Try {n_try}: {next}")

    return n_try