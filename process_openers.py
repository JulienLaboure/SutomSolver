# IN PROGRESS

from sutom_solver import *

def find_best_opener():
    first_char = input("First character : ")
    nb_chars = int(input("Number of characters : "))

    all_propositions = get_words_list(first_char, nb_chars)
    best_opener = new_step(all_propositions, all_propositions)

    return best_opener

print(find_best_opener())