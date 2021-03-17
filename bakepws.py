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


# filter duplicate words in wordlist
def filter_lists(wordlist):
    for idx_word, word in enumerate(wordlist):
        curr_word = word
        for idx_other_word, other_word in enumerate(wordlist):
            if other_word == curr_word and idx_word != idx_other_word:
                wordlist.remove(other_word)

    return wordlist


def parse_line(line):
    line = line.split()
    return re.escape(line[0].strip())


def gen_lists_hcat(wordlist, rule, hashcat_path='/bin/hashcat'):
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

        for line in file:
            line = parse_line(line)
            gen_words = os.popen("{} {} | {} -r {} --stdout"
                                 "".format(echo_path, line, hashcat_path, rule)).read()
            gen_list = gen_words.split()
            gen_list = filter_lists(gen_list)
            lists.append(gen_list)

    except FileNotFoundError:
        print("Couldn't find wordlist.")
        exit()
    except:
        print("Something went wrong. Please submit this issue")
        exit()
    finally:
        file.close()

    return lists


def gen_list(wordlist):
    gen_list = []

    try:
        file = open(wordlist, 'r')

        for line in file:
            line = parse_line(line)
            gen_list.append([line])
    except FileNotFoundError:
        print("Couldn't find wordlist.")
        exit()
    finally:
        file.close()

    return filter_lists(gen_list)


def combine_words(lists, outfile):
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

    usage = 'Creating a password-list with ease. \n' \
            '\n' \
            'Usage:\n' \
            'python3 bakepws.py [OPTIONS] -i <input-file>\n' \
            '\n' \
            'With no output file, print to standard output\n' \
            '\n' \
            '      -i:     path/to/input.file\n' \
            '      -r:     path/to/hashcat.rule\n' \
            '      -o:     path/to/output.file\n' \
            '   --cat:     path/to/hashcat\n' \
            '\n' \
            'Examples:\n' \
            'python3 bakepws.py -i examples/dough.txt\n' \
            'python3 bakepws.py -i examples/dough.txt -r examples/recipe.rule -o examples/cake.txt\n'

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

    if wordlist == "":
        print(usage)
        exit()

    return wordlist, rule, outfile, hashcat_path


if __name__ == '__main__':
    wordlist, rule, outfile, hashcat_path = get_args()

    if hashcat_path == "" and rule == "":
        lists = gen_list(wordlist)
    elif hashcat_path == "":
        lists = gen_lists_hcat(wordlist, rule)
    else:
        lists = gen_lists_hcat(wordlist, rule, hashcat_path)

    combine_words(lists, outfile)
