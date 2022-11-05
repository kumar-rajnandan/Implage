import os
import sys

class mainnode:
    def __init__(self, letter=None, isTerminal=False):
        self.letter = letter
        self.isTerminal = isTerminal
        self.childnode = {}


class Trie:
    def __init__(self):
        self.root = mainnode()
        self.counts = {}

    def selfInsert(self, word):
        current = self.root
        for letter in word:
            if letter not in current.childnode:
                current.childnode[letter] = mainnode(letter)
            current = current.childnode[letter]
        current.isTerminal = True

    def __contains__(self, word):
        current = self.root
        for letter in word:
            if letter not in current.childnode:
                return False
            current = current.childnode[letter]
        return current.isTerminal

    def decompose(self, word):
        if not word:
            return 0, []
        if word in self.counts:
            return self.counts[word]
        current = self.root
        for index, letter in enumerate(word):
            if letter not in current.childnode:
                return 0, []
            current = current.childnode[letter]
            if current.isTerminal:
                suffix = word[index + 1:]                          
                suffix_count, suffix_list = self.decompose(suffix)  
                self.counts[suffix] = suffix_count, suffix_list     
                if suffix_count:                                    
                    return 1 + suffix_count, [word[:index + 1]] + suffix_list 
        return current.isTerminal, [word]

    def getCompound(self, word):
        decompose_num, decompose_list = self.decompose(word)
        return decompose_num > 1, decompose_num, decompose_list

def inputFile(filename):
    words = []
    trie = Trie()
    with open(filename, 'r') as f:
        for line in f:
            word = line.strip()
            trie.selfInsert(word)
            words.append(word)
    return trie, words

def initListItems(compoundList):
    compoundList.sort(key = lambda tup: len(tup[0]), reverse=True)
    return compoundList


def getCompoundList(trie, words):
    compound = []
    for word in words:
        isValid, num, dlist = trie.getCompound(word)
        if isValid:
            compound.append((word, num, dlist))
    return compound

def finalExecute(filename='input_01.txt'):
    trie, words = inputFile(filename)
    compoundList = initListItems(getCompoundList(trie, words))

    longestWord = compoundList[0][0]
    secondLongesCompoundtWord = compoundList[1][0]

    if len(longestWord):
        print( "Longest compound word found is: \t\"" + longestWord + "\"")
    else:
        print( "No largest compound words exist in this list.")
    if len(secondLongesCompoundtWord):
        print( "Second Longest compound word found is: \t\"" + secondLongesCompoundtWord + "\"")
    else:
        print( "No second largest compound words exist in this list.")

    return trie, words, compoundList

finalExecute('Input_02.txt')