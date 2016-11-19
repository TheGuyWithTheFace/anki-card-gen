#!/usr/bin/python
import sys

#See thoughts.txt file for expected input format.

_mappings = {}

def main():
    global _mappings

    # maps "pinyin chars" (0-9 and symbols) to actual tone such as é and ī
    _mappings = load_mappings("mappings.txt")

    # For now use hardcoded things, later we'll make a nicer ui maybe
    f = open("input.csv", newline='')
    parse_input(f)

    print(_mappings)


def parse_input(input_file):
    """Reads input "csv" (not a real csv), returns list of dictionaries."""

    vocab = []

    for line in list(input_file):
        items = line.split(',')
        # Problem: items may have multiple definitions separated by commas
        # Solution: Look for (hopefully unique) Chinese character + pinyin combination
        #    in items. pinyin is always the next item after the character, and should
        #    always have a tone_count equal to the number of characters in chinese


        character_index = 1 # delete me
        """
        character_index = -1
        for i in range(items-1):
            first = items[i]
            second = items[i+1]
            if(len(first) == tone_count(second)):
                character_index = i
                break
        
        if(character_index = -1):
            print(line)
            break
        """

        term = {}
        # meaning must be every value before the character 
        term["meaning"] = ', '.join(items[i] for i in range(character_index))

        term["character"] = items[character_index]

        # pinyin comes right after character
        term["pinyin"] = format_pinyin(items[character_index+1])

        vocab.append(term)

    # test code pls ignore
    for word in vocab:
        print(word["character"], word["meaning"], word["pinyin"]) 

    return vocab

def format_pinyin(word):
    """Converts pinyin tone encodings in word to accented characters for readability"""

    global _mappings

    for c in word:
        if(c in _mappings):
            word = word.replace(c, _mappings[c])
            print("replace")

    return word 

# We will use this to determine where everything else is in each line of input
def tone_count(word):
    """Returns the number of characters in word that are used for pinyin tone encoding"""
    pass  #TODO

def load_mappings(filename):
    mapfile = open(filename, "r")
    maps = {}
    for line in mapfile.read().splitlines():
        line = line.split(' ')
        maps[line[0]] = line[1]

    return maps

main()