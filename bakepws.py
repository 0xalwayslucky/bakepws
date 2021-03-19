#!/usr/bin/env python3

"""
Creating a password-list with ease.
Hashcat has to be installed in order to work with rules.

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

        file.close()

    except FileNotFoundError:
        print("Couldn't find wordlist.")
        exit()
    except:
        print("Something went wrong. Please submit this issue")
        exit()

    return lists


def gen_list(wordlist):
    gen_list = []

    try:
        file = open(wordlist, 'r')

        for line in file:
            line = parse_line(line)
            gen_list.append([line])

        file.close()
    except FileNotFoundError:
        print("Couldn't find wordlist.")
        exit()

    return filter_lists(gen_list)


# start & end is the range of how many words to combine
# e.g. 0 and 4 would combine up to 4 words (including combinations below 4)
def combine_words(lists, start, end):
    permutation_lists = []
    product_lists = []
    password_list = ""

    for i in range(start+1, end+2):
        for tpl in list(itertools.permutations(lists, i)):
            permutation_lists.append(list(tpl))

    for li in permutation_lists:
        product_lists.append(list(itertools.product(*li)))

    for index, product in enumerate(product_lists):
        for pl_index, plist in enumerate(product_lists[index]):
            string = ''
            for element in plist:
                string += str(element)

            password_list += string.strip() + '\n'

    return password_list.rstrip()


def output(string, outfile):
    if outfile:
        try:
            file = open(outfile, 'w')
            try:
                file.write(string)
            finally:
                file.close()
        except FileNotFoundError as fnfe:
            print("Error in output: {}".format(fnfe))
            exit()
        except IOError as ioe:
            print("Error in output: {}".format(ioe))
            exit()
    else:
        print(string)


def get_args():
    argv = sys.argv[1:]
    wordlist = ""
    rule = ""
    outfile = ""
    hashcat_path = ""
    start = -1
    end = -1
    c_set = False
    a_set = False

    usage = 'Creating a password-list with ease. \n' \
            '\n' \
            'Usage:\n' \
            'python3 bakepws.py [OPTIONS] -i <input-file>\n' \
            '\n' \
            'With no output file, print to standard output\n' \
            '\n' \
            '      -i:     Specify an input file\n' \
            '      -r:     Specify a hashcat rule\n' \
            '      -o:     Specify an output file\n' \
            '      -a:     Print all words and combinations\n' \
            '      -c:     Combine exactly n word(s)\n' \
            '   --min:     Specify minimum amount of combinations\n' \
            '   --max:     Specify maximum amount of combinations\n' \
            '   --cat:     Specify a custom hashcat path\n' \
            '\n' \
            'Examples:\n' \
            'python3 bakepws.py -i examples/dough.txt\n' \
            'python3 bakepws.py -i examples/dough.txt -r examples/recipe.rule -a\n' \
            'python3 bakepws.py -i examples/dough.txt -r examples/recipe.rule -o examples/cake.txt\n'

    try:
        opts, args = getopt.getopt(argv, "i:r:o:ac:", ['cat=', 'min=', 'max='])

        for opt, arg in opts:
            if opt in ['-i']:
                wordlist = arg
            elif opt in ['-r']:
                rule = arg
            elif opt in ['-o']:
                outfile = arg
            elif opt in ['-a']:
                start = 0
                a_set = True
            elif opt in ['-c']:

                if a_set:
                    continue

                if int(arg) < 0:
                    raise ValueError

                start = int(arg)
                end = int(arg)
                c_set = True

            elif opt == '--min':

                if c_set or a_set:
                    continue

                if int(arg) < 0:
                    raise ValueError

                start = int(arg)

            elif opt == '--max':

                if c_set or a_set:
                    continue

                if int(arg) < 0:
                    raise ValueError

                end = int(arg)

            elif opt == '--cat':
                hashcat_path = arg
    except:
        print('Invalid syntax.')
        exit()

    if wordlist == "":
        print(usage)
        exit()

    return wordlist, rule, outfile, hashcat_path, start, end


if __name__ == '__main__':
    wordlist, rule, outfile, hashcat_path, start, end = get_args()

    if hashcat_path == "" and rule == "":
        lists = gen_list(wordlist)
    elif hashcat_path == "":
        lists = gen_lists_hcat(wordlist, rule)
    else:
        lists = gen_lists_hcat(wordlist, rule, hashcat_path)

    # if start and end weren't set, combine all words from input
    if start == -1 and end == -1:
        start = len(lists)-1
        end = len(lists)-1
    # if end has been set default start to 0
    elif end != -1 and start == -1:
        start = 0
    # if start has been set default end to length list
    elif end == -1 and start != -1:
        end = len(lists)-1

    if start > len(lists)-1:
        start = len(lists)-1

    if end > len(lists)-1:
        end = len(lists)-1

    password_list = combine_words(lists, start, end)
    output(password_list, outfile)
