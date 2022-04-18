from constraint_prog import get_words, solve_worlde
from genetic_algo import solve_wordle_GA

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch Wordle solver')
    parser.add_argument("--algo", type=str, default="constraint_prog",
                        choices=["constraint_prog", "genetic_algo"],
                        help="type of algorithm using to solve")
    parser.add_argument("--secret-word", type=str, default="house", 
                        help="secret word")
    args = parser.parse_args()

    algo, secret_word = args.algo, args.secret_word
    words = get_words()

    print(f"Algo: {algo}\nSecret word: {secret_word}")

    if algo == "constraint_prog":
        solve_worlde(secret_word, words)
    else:
        solve_wordle_GA(words, secret_word)
