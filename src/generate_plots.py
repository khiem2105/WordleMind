from constraint_prog import solve_worlde, get_secret_word, get_words
from genetic_algo import solve_wordle_GA

if __name__ == "__main__":
    import time
    from collections import defaultdict
    import matplotlib.pyplot as plt

    n_try = defaultdict(lambda :0)
    times = defaultdict(lambda :0)

    words = get_words()

    for n in range(4, 10):
        print(f"{n}:")
        for i in range(20):
            if i % 5 == 0:
                print("+")
            else:
                print(".")
            secret_word = get_secret_word(words, n)
            start = time.time()
            n_try[n] += solve_worlde(secret_word, words, verbose=False)
            times[n] += time.time() - start

    plt.figure()
    plt.plot(range(4, 10), [n / 20 for n in n_try.values()])
    plt.title("Number of try with 20 re-runs using constraint programming")
    plt.xlabel("Length of secret word")
    plt.ylabel("n.try")
    plt.savefig("plots/n_csp.png")

    plt.figure()
    plt.plot(range(4, 10), [t / 20 for t in times.values()])
    plt.title("Execution time with 20 re-runs using constraint programming")
    plt.xlabel("Length of secret word")
    plt.ylabel("s")
    plt.savefig("plots/t_csp.png")

    n_try_ga = defaultdict(lambda :0)
    times_ga = defaultdict(lambda :0)

    for n in range(4, 10):
        print(f"n={n}:")
        for i in range(3):
            secret_word = get_secret_word(words, n)
            start = time.time()
            n_try_ga[n] += solve_wordle_GA(words, secret_word, verbose=False)
            times_ga[n] += time.time() - start

    plt.figure()
    plt.plot(range(4, 10), [n / 3 for n in n_try_ga.values()])
    plt.title("Number of try with 3 re-runs using GA")
    plt.xlabel("Length of secret word")
    plt.ylabel("n.try")
    plt.savefig("plots/n_ga.png")

    plt.figure()
    plt.plot(range(4, 10), [t / 3 for t in times_ga.values()])
    plt.title("Execution time with 3 re-runs using GA")
    plt.xlabel("Length of secret word")
    plt.ylabel("s")
    plt.savefig("plots/t_ga.png")

    plt.figure()
    plt.plot(range(4, 10), [n / 3 for n in n_try_ga.values()], label="GA")
    plt.plot(range(4, 10), [n / 20 for n in n_try.values()], label="CSP")
    plt.title("Compare CSP and GA in number of try")
    plt.xlabel("Length of secret word")
    plt.ylabel("n.try")
    plt.legend()
    plt.savefig("plots/n_ga_vs_csp.png")

    plt.figure()
    plt.plot(range(4, 10), [t / 3 for t in times_ga.values()], label="GA")
    plt.plot(range(4, 10), [t / 20 for t in times.values()], label="CSP")
    plt.title("Compare CSP and GA in execution time")
    plt.xlabel("Length of secret word")
    plt.ylabel("s")
    plt.legend()
    plt.savefig("plots/t_ga_vs_csp.png")