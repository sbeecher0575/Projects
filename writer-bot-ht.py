'''
    file: writer-bot-ht.py
    author: Stephen Beecher
    class: CSC120 spring 2019
    Purpose: Use the Markov Chain Algorithm to randomly generate text based on a given file. A new file is created with the format new_filename.txt
'''

import random

SEED = input('seed: ')

class Hashtable:
    '''
    This class is used to keep several key value pairs in the form of a hashtable.
    '''
    def __init__(self, size):
        '''
        This method initializes the size of the hashtable and fills the hashtable of length size with None

        Parameters: self: the Hashtable object
                    size: int, the length of the hashtable
        Returns:    None

        Pre-condition:  size has to be an int
        Post-condition: the hashtable is created
        '''
        self._size = size
        self._pairs = [None] * size

    def pairs(self):
        return self._pairs

    def size(self):
        return self._size

    def _hash(self, key):
        '''
        This method is used to hash a string and get a number to be the index in the hashtable.

        Parameters: self: the Hashtable object
                    key: a str, the string to hash
        Returns:    an int, the hashed value

        Pre-condition:  key has to be a str
        Post-condition: the return value is an int less than self.size()
        '''
        p = 0
        for c in key:
            p = 31*p + ord(c)
        return p % self.size()
    
    def put(self, key, value):
        '''
        This method is used to put a key value pair into the hashtable.

        Parameters: self: the Hashtable object
                    key: a str, the prefix to input
                    value: a list, the relating suffixes to the prefix
        Returns:    None

        Pre-condition:  key is not in the hashtable already.
        Post-condition: the key value pair is now in the hashtable.
        '''
        i = self._hash(key)
        while (self.pairs())[i] != None:
            i = i - 1
        self.pairs()[i] = [key, value]

    def get(self, key):
        '''
        This method is used to get the value corresponding to the key argument.

        Parameters: self: the Hashtable object
                    key: a str, the prefix to search the hashtable with
        Returns: the value associated with the key, or None if the key is not in the hashtable

        Pre-condition:  none
        Post-condition: the return value is the list of suffixes or None.
        '''
        for pair in self.pairs():
            if pair == None:
                continue
            if pair[0] == key:
                return pair[1]
        return None

    def __contains__(self, key):
        '''
        This method is used to determine whether or not a key is in the hashtable

        Parameters: self: the Hashtable object
                    key: a str, the key to search
        Returns:    True if key is in the Hashtable and False if it is not

        Pre-condition:  none
        Post-condition: The return value is Boolean
        '''
        for pair in self.pairs():
            if pair == None:
                continue
            if pair[0] == key:
                return True
        return False


    def __str__(self):
        '''
        This method is used to represent a hashtable as a string.

        Parameters: self: the Hashtable object
        Returns:    a string where it prints out each pair, one per line.

        Pre-condition:  none
        Post-condition: the Hashtable can now be represented by a string
        '''
        string = ''
        for pair in self.pairs():
            string += str(pair) + '\n'
        return string


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


def create_hashtable(wordlist, n, length):
    '''
    This function takes a list of words and a prefix length and maps the prefix to a list of suffixes using a dictionary.

    Parameters: wordlist: a list of strings
                n: an int, the prefix length
                length: the length of the hashtable
    Returns:    a hashtable in the form [[prefix_string_1: [suffix1, ... ]], ...]
    
    Pre-condition:  wordlist is a list of strings and n is an int greater than 0.
    Post-condition: Return value is a hashtable with the keys as strings and the values as lists.
    '''
    hashtable = Hashtable(length)
    for i in range(n, len(wordlist)):
        prefixlst = wordlist[i-n:i]
        prefixstr = ''
        for word in prefixlst:
            prefixstr += (word + ' ')
        prefixstr = prefixstr.strip()
        if prefixstr in hashtable:
            hashtable.get(prefixstr).append(wordlist[i])
        else:
            hashtable.put(prefixstr, [wordlist[i]])
    return hashtable


def create_new_list(hashtable, n, text_size):
    '''
    This function takes a dictionary and randomly generates a list of words of a given length.

    Parameters: hashtable: a hashtable in with strings of prefixes as keys and lists of suffixes as values.
                n: an int, the prefix length
                text_size: the number of words in the output list
    Returns:    a list of randomly generated words using the Markov chain algorithm

    Pre-condition: hashtable has strings with n words as keys and lists of words as values, n and text_size are ints greater than zero
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
        lst = newlist[i-n:]
        key = ''
        for item in lst:
            key += (item + ' ')
        key = key.strip()
        options = hashtable.get(key)
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
    length = int(input('length of hashtable: '))
    n = int(input('prefix length: '))

    if n < 1:
        print("ERROR: specified prefix size is less than one")
        exit()
    wordlist = readfile(filename, n)
    text_size = int(input('Length of text: '))
    if text_size < 1:
        print("ERROR: specified size of the generated text is less than one")
        exit()
    hashtable = create_hashtable(wordlist, n, length)
    lst = create_new_list(hashtable, n, text_size)
    output = format_list(lst)
    newfile = open('new_' + filename, 'w')
    newfile.write(output.strip())
    newfile.close()

main()