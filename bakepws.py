#!/usr/bin/env python3

"""
Creating a password list with hashcat rules
Hashcat has to be installed in order to work

Hashcat: https://github.com/hashcat
Author: https://github.com/0xalwayslucky
"""

import os
import sys
import itertools
import re
import getopt


def gen_lists(wordlist, rule, hashcat_path='/bin/hashcat'):
    lists = []
    echo_path = '/bin/echo'

    if not os.path.isfile(rule):
        print("Couldn't find hashcat rule.")
        exit()

    if not os.path.isfile(hashcat_path):
        if os.path.isfile('/usr{}'.format(hashcat_path)):
            hashcat_path = '/usr{}'.format(hashcat_path)
        else:
            print("Invalid path to hashcat executable. If it is please specify a custom path with --cat")
            exit()

    if not os.path.isfile(echo_path):
        print("Couldn't find executable {}".format(echo_path))
        exit()

    try:
        file = open(wordlist, 'r')
    except:
        print("Couldn't open wordlist.")
        exit()

    for line in file:
        line = line.split()
        line = line[0].strip()
        line = re.escape(line)
        gen_words = os.popen("{} {} | {} -r {} --stdout"
                             "".format(echo_path, line, hashcat_path, rule)).read()
        gen_list = gen_words.split()

        # filter duplicate words in list
        for idx_word, word in enumerate(gen_list):
            curr_word = word
            for idx_other_word, other_word in enumerate(gen_list):
                if other_word == curr_word and idx_word != idx_other_word:
                    gen_list.remove(other_word)

        lists.append(gen_list)

    file.close()
    return lists


def gen_modded_list(lists, outfile):
    permutation_lists = []
    product_lists = []

    for tpl in list(itertools.permutations(lists)):
        permutation_lists.append(list(tpl))

    for li in permutation_lists:
        product_lists.append(list(itertools.product(*li)))

    if outfile:
        try:
            file = open(outfile, 'w')
        except:
            print("Couldn't open output file.")
            exit()

    for index, product in enumerate(product_lists):
        for pl_index, plist in enumerate(product_lists[index]):
            string = ''
            for element in plist:
                string += str(element)

            # If the current string is the last element of the last list in product_lists: don't append a newline
            if index == len(product_lists) - 1 and len(product_lists[len(product_lists) - 1]) - 1 == pl_index:
                string = string.strip()
            else:
                string = string.strip() + "\n"

            if outfile:
                file.write(string)
            else:
                print(string.strip())

    if outfile:
        file.close()


def get_args():
    argv = sys.argv[1:]
    wordlist = ""
    rule = ""
    outfile = ""
    hashcat_path = ""

    usage = 'Creating a password list with hashcat rules. \n' \
            '\n' \
            'Description:\n' \
            'This tool takes words seperated by newlines from a file,\n' \
            'generates for each word a list based on the hashcat rules supplied (using hashcat) and\n' \
            'creates a wordlist with all possible combinations of the words that have been generated.\n' \
            'Mmmmmm delicious.\n' \
            '\n' \
            'Usage:\n' \
            'python3 bakepws.py -i <input-file> -r <hashcat-rule>\n' \
            '\n' \
            'With no output file, print to standard output\n' \
            '\n' \
            '-i:        path/to/input.file\n' \
            '-r:        path/to/hashcat.rule\n' \
            '-o:        path/to/output.file\n' \
            '--cat:     path/to/hashcat\n' \
            '\n' \
            'example:\n' \
            'python3 bakepws.py -i examples/dough.txt -r examples/recipe.rule -o examples/cake.txt' \
            '\n' \

    try:
        opts, args = getopt.getopt(argv, "i:r:o:", ['cat='])
    except:
        print('Invalid syntax.')
        exit()

    for opt, arg in opts:
        if opt in ['-i']:
            wordlist = arg
        elif opt in ['-r']:
            rule = arg
        elif opt in ['-o']:
            outfile = arg
        elif opt == '--cat':
            hashcat_path = arg

    if wordlist == "" or rule == "":
        print(usage)
        exit()

    return wordlist, rule, outfile, hashcat_path


if __name__ == '__main__':
    wordlist, rule, outfile, hashcat_path = get_args()

    if hashcat_path == "":
        lists = gen_lists(wordlist, rule)
    else:
        lists = gen_lists(wordlist, rule, hashcat_path)

    gen_modded_list(lists, outfile)
