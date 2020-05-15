# Standard Library
import random
import requests

# Third party
from bs4 import BeautifulSoup

# Custom
from config import key


def algebra():
    """ Constructs a random algebra problem
    """
    operators = ["+", "-", "*", "/"]
    problem = ""

    for i in range(4):
        number = random.randint(1,9)
        op = random.choice(operators)
        problem += str(number)
        if i != 3:
            problem += f" {op} "

    solution = eval(problem)
    problem = problem.replace("+", "plus").replace("-", "minus").replace("*", "times").replace("/", "divided by")
    return (problem, solution)


def get_synonyms(word="light"):
    """ Returns Top 10 synonyms for a given word.
    https://dictionaryapi.com/products/api-collegiate-thesaurus
    """
    url = f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={key}"
    response = requests.get(url)
    syn_batch = response.json()[0]["meta"]["syns"]

    word_count = 0
    synonyms = ""
    for syn_list in syn_batch:
        for word in syn_list:
            if word_count < 10:
                # print(word)
                synonyms += (word + "\n")
                word_count += 1
            else:
                break
    return synonyms

# TODO This is terrible, work on this.
def number_sequence():
    """Generates random number sequence
    Patterns = num |op| num
        num |op| (num |op| num)
        num |op| randomint
    """
    number = random.randint(1,9)
    operators = ["+", "-"]
    operator = random.choice(operators)
    sequence = f"{number}"
    
    def algo_1(sequence, number):
        for i in range(6):
            calc = f"{number} {operator} {number}"
            result = eval(calc)
            sequence += f" {result} "
            number = result
        return sequence

    algos = [algo_1]
    algo = random.choice(algos)
    sequence = algo(sequence, number)
    answer = eval(f"{number} {operator} {number}")
    print(answer)
    return sequence


def digit_span(span=10):
    """Returns a given number of digits between 1 and 9
    :param int: span -> the number of digits
    """
    digits = ""
    for _ in range(span):
        digits += str(random.randint(1,9)) + ". "
    return digits

def draw_an_idiom():
    url = "https://randomword.com/idiom"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    idiom = soup.find(id='random_word')
    definition = soup.find(id='random_word_definition')
    results = (idiom.text, definition.text)
    return results

