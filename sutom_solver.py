from math import *

class Results:

    def __init__(self, nb_chars, N):
        reds = [0]
        yellows = []
        whites = []
        for i in range(1, nb_chars):
            result = N % 3
            if result == 0:
                whites.append(i)
            elif result == 1:
                yellows.append(i)
            else:
                reds.append(i)
            N = N // 3
        self.reds = reds
        self.yellows = yellows
        self.whites = whites

class Answer:

    def __init__(self, word, results):
        self.word = word
        self.results = results

    def is_correlated_with(self, word):
        if len(word) != len(self.word):
            raise Exception("Compared words {} and {} have not the same size".format(self.word, word))
        
        processed_word = list(word)

        for position in self.results.reds:
            if self.word[position] != processed_word[position]:
                return False
            processed_word[position] = '@'

        for position in self.results.yellows + self.results.whites:
            if self.word[position] == processed_word[position]:
                return False

        for position in self.results.yellows:
            has_yellow = False
            for character in range(len(processed_word)):
                if self.word[position] == processed_word[character]:
                    has_yellow = True
                    processed_word[character] = '@'
                    break
            if not has_yellow:
                return False

        for position in self.results.whites:
            for character in range(len(processed_word)):
                if self.word[position] == processed_word[character]:
                    return False

        return True

def get_answer(word):
    results = []
    for position in range(len(word)):
        results.append(input("Color result for character {} : ".format(position + 1)))
    return Answer(word, Results(len(word), results_list_to_int(results)))

def word_pair_to_int(word, solution):
    processed_word = list(word)
    processed_solution = list(solution)

    colors = ['w' for i in range(len(word))]

    for position in range(len(word)):
        if processed_word[position] == processed_solution[position]:
            colors[position] = 'r'
            processed_solution[position] = '@'
    
    for position in range(len(word)):
        if colors[position] != 'r':
            for position2 in range(len(solution)):
                if position != position2 and processed_word[position] == processed_solution[position2]:
                    colors[position] = 'y'
                    processed_solution[position2] = '@'

    code = 0
    for position in range(1, len(word)):
        if colors[position] == 'r':
            code += 2 * (3**(position - 1))
        elif colors[position] == 'y':
            code += (3**(position - 1))

    return code

            
def results_list_to_int(list):
    if list[0] != 'r':
        raise Exception("First character should be the same")
    code = 0
    for position in range(1, len(list)):
        if list[position] == 'r':
            code += (2 * (3**(position - 1)))
        elif list[position] == 'y':
            code += (1 * (3**(position - 1)))
        elif list[position] == 'w':
            code += (0 * (3**(position - 1)))
        else:
            raise Exception("Available colors are 'r', 'y' and 'w'")
    return code


def get_words_list(first_char, nb_chars):
    dictionnary = open('mots.txt', 'r', encoding='utf8').read().splitlines()
    words_list = []
    for word in dictionnary:
        if word[0] == first_char and len(word) == nb_chars:
            words_list.append(word)
    return words_list

def update_possible_words(possible_words, new_answer):
    new_possible_words = []
    for word in possible_words:
        if new_answer.is_correlated_with(word):
            new_possible_words.append(word)
    return new_possible_words

def new_step(possible_words, all_propositions):
    best_word = ''
    max_information = 0

    for word in all_propositions:
        informations = []
        for i in range(3**(len(word) - 1)):
            informations.append(0)

        for possible_word in possible_words:
            informations[word_pair_to_int(word, possible_word)] += 1
            pass

        information = 0
        for i in range(3**(len(word) - 1)):
            probability = informations[i]/len(possible_words)
            if probability != 0:
                information -= (probability * log2(probability))

        print(word, " : ", information)

        if information > max_information:
            max_information = information
            best_word = word
            print("NEW BEST WORD : ", best_word)

    if best_word == '':
        raise Exception("No possible word")
    return best_word

def main():

    first_char = input("First character : ")
    nb_chars = int(input("Number of characters : "))

    all_propositions = get_words_list(first_char, nb_chars)
    possible_words = all_propositions.copy()
    while True:
        new_word = new_step(possible_words, all_propositions)
        print("Word : ", new_word)
        new_answer = get_answer(new_word)
        possible_words = update_possible_words(possible_words, new_answer)
        if len(possible_words) == 1:
            print("Word : ", possible_words[0])
            return