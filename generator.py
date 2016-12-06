#!/usr/bin/python
import csv

#See thoughts.txt file for expected input format.

_mappings = {}
_tags = {}

def main():
    global _mappings
    global _tags

    # maps "pinyin chars" (0-9 and symbols) to actual tone such as é and ī
    _mappings = load_mappings("mappings.txt")
    # maps letters such as n., v., to words such as noun and verb
    _tags = load_tags("tags.txt")

    # For now use hardcoded things, later we'll make a nicer ui maybe
    f = open("input.csv", newline='')
    parse_input(f)


def parse_input(input_file):
    """Reads input "csv" (not a real csv), returns list of dictionaries."""

    vocab = []

    tags = [];

    currentline = 1

    for line in list(input_file):
        items = [x.strip() for x in line.split(',')]
        # Problem: items may have multiple definitions separated by commas
        # Solution: Look for (hopefully unique) Chinese character + pinyin combination
        #    in items. pinyin is always the next item after the character, and should
        #    always have a tone_count equal to the number of characters in chinese


        character_index = -1
        for i in range(len(items)-1):
            first = items[i].strip()
            second = items[i+1].strip()
            if(len(first) == tone_count(second)):
                character_index = i
                break
        
        if(character_index == -1):
            print("Error parsing line: " + line)
            currentline += 1
            continue

        term = {}
        # meaning must be every value before the character 
        term["meaning"] = ', '.join(items[i] for i in range(character_index))

        term["character"] = items[character_index]

        # pinyin comes right after character
        term["pinyin"] = format_pinyin(items[character_index+1])

        # get all relevant tags
        i = character_index + 2
        tags = []
        while('L' not in items[i]):
            tags.append(format_tag(items[i]))
            i += 1

        # Add lesson tag
        lesson = "V3_Ch" + items[i][3:]
        tags.append(lesson)

        term["tags"] = ' '.join(tags)
        vocab.append(term)

        # guess at sound file name
        term["sound"] = "[sound:" + lesson + "_" + str(currentline) + ".wav]"
        currentline += 1


    dump_dict(vocab, "output.csv")

    return vocab

def format_tag(word):

    global _tags
    if word in _tags:
        return _tags[word]
    else:
        print("WARNING: Unrecognized tag '" + word + "'")
        return word

def format_pinyin(word):
    """Converts pinyin tone encodings in word to accented characters for readability"""

    global _mappings

    for c in word:
        if(c in _mappings):
            word = word.replace(c, _mappings[c])

    return word 

# We will use this to determine where everything else is in each line of input
def tone_count(word):
    """Returns the number of characters in word that are used for pinyin tone encoding"""
    count = 0
    global _mappings

    # words describing lesson count and page # give incorrect input since they have numbers
    if "L. " in word or "p. " in word:
        return 0

    for c in word:
        if c in _mappings and "L" not in word:
            count += 1

    return count

def dump_dict(itemarray, filename):
    """Dumps an array of dictionaries into a .csv file named filename"""
    # init csv file
    f = open(filename, 'w')
    writer = csv.DictWriter(f, fieldnames=list(itemarray[0].keys()))
    writer.writeheader()

    # write everything in items to csv
    for rowdata in itemarray:
        writer.writerow(rowdata)

def load_tags(filename):
    tagfile = open(filename, "r")
    tags = {}
    for line in tagfile.read().splitlines():
        line = line.split(' ')
        tags[line[0]] = ' '.join(line[1:])

    return tags

def load_mappings(filename):
    mapfile = open(filename, "r")
    maps = {}
    for line in mapfile.read().splitlines():
        line = line.split(' ')
        maps[line[0]] = line[1]

    return maps

main()
