'''
    File: writer-bot.py
    Author: Stephen Beecher
    Purpose: Use the Markov Chain Algorithm to randomly generate text based on a given file.
'''

import random

SEED = input('seed: ')

def readfile(filename, n):
    '''
    This function reads a file and returns a list of words in that file.

    Parameters: filename: a str, the name of file
                n: an int, the prefix length
    Returns:    A list of strings, all the words in the file, punctuation included.

    Pre-condition: filename is the name of a file in the same directory, and n is an int greater than 0.
    Post-condition: The return value is a list of strings.
    '''
    file = open(filename)
    wordlist = []
    for i in range(n):
        wordlist.append('NONWORD')
    for line in file:
        lst = line.strip().split()
        for item in lst:
            wordlist.append(item)
    for i in range(n):
        wordlist.append('NONWORD')
    return wordlist

def create_dict(wordlist, n):
    '''
    This function takes a list of words and a prefix length and maps the prefix to a list of suffixes using a dictionary.

    Parameters: wordlist: a list of strings
                n: an int, the prefix length
    Returns:    a dictionary in the form {(prefix1, ... ): [suffix1, ... ], ...}
    
    Pre-condition:  wordlist is a list of strings and n is an int greater than 0.
    Post-condition: Return value is a dict with the keys as tuples and the values as lists.
    '''
    dictionary = {}
    for i in range(n, len(wordlist)):
        prefix = tuple(wordlist[i-n:i])
        if prefix in dictionary:
            dictionary[prefix].append(wordlist[i])
        else:
            dictionary[prefix] = [wordlist[i]]
    return dictionary

def create_new_list(dictionary, n, text_size):
    '''
    This function takes a dictionary and randomly generates a list of words of a given length.

    Parameters: dictionary: a dict in with tuples of prefixes as keys and lists of suffixes as values.
                n: an int, the prefix length
                text_size: the number of words in the output list
    Returns:    a list of randomly generated words using the Markov chain algorithm

    Pre-condition: dictionary has tuples of length n as keys and lists of words as values, n and text_size are ints greater than zero
    Post-condition: The return value is a list of randomly generated words using the Markov chain algorithm
    '''
    random.seed(SEED)
    newlist = []
    for i in range(n):
        newlist.append('NONWORD')
    output = []
    i = n
    while True:
        if len(output) == text_size:
            return output
        key = tuple(newlist[i-n:])
        options = dictionary[key]
        if len(options) == 1:
            addition = options[0]
        else:
            addition = options[random.randint(0, len(options)-1)]
        newlist.append(addition)
        if addition != 'NONWORD':
            output.append(addition)
        i += 1
    
def format_list(wordlist):
    '''
    This function takes a list of words and formats it into a string with a new line every 10 words

    Parameters: wordlist: a list of words
    Returns: a string with a space between all of the words and a newline every 10 words

    Pre-condition: wordlist is a list of strings
    Post-condition: the return value is a single string.
    '''
    string = ''
    for i in range(len(wordlist)):
        if wordlist[i] != 'NONWORD':
            if (i + 1) % 10 != 0:
                string += (wordlist[i] + ' ')
            else:
                string += (wordlist[i] + '\n')
    return string

def main():
    filename = input('filename: ')
    n = int(input('prefix size: '))
    assert n > 0
    wordlist = readfile(filename, n)
    text_size = int(input('length of text: '))
    assert text_size > 0
    dictionary = create_dict(wordlist, n)
    lst = create_new_list(dictionary, n, text_size)
    output = format_list(lst)
    newfile = open('new_' + filename, 'w')
    newfile.write(output.strip())
    newfile.close()
    

main()