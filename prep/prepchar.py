#!/usr/bin/env python

""" Script to modify contents of character file """

import os
import re
import sys


def usage():
    print("prepchar.py source_file target_file [health_multiplier]")
    sys.exit(1)


def get_options(args):
    """ Returns options from command line """
    multiplier = 2
    nargs = len(sys.argv)
    if nargs == 3:
        source = sys.argv[1]
        if not os.path.exists(source):
            print(f"No such file: {source}")
            sys.exit(2)
        target = sys.argv[2]
    elif nargs == 4:
        multiplier = sys.argv[3]
        if not multiplier.isnumeric():
            usage()
    else:
        usage()

    return source, target, multiplier


def prepare_char_file(source, target, multiplier):
    """ Prepares new character file """
    with open(source, "r") as f:
        with open(target, "w") as t:
            for line in f.readlines():
                m = re.match(
                    r'data "(?P<key>Vitality|Passives)" "(?P<value>[^"]+?)[; ]*"', line)
                if m:
                    key = m.group('key')
                    value = m.group('value')

                    if value.isnumeric():
                        value = int(m.group('value'))
                        if 1 < value < 1000:
                            value *= multiplier
                    else:
                        value += ';DifficultyBonus'

                    t.write(f'data "{key}" "{value}"\n')
                else:
                    t.write(line)


if __name__ == "__main__":
    opts = get_options(sys.argv)
    prepare_char_file(*opts)
