#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os


BASH_ATTRIBUTES = {"regular": "0",
                   "bold": "1", "underline": "4", "strike": "9",
                   "light": "1", "dark": "2",
                   "invert": "7"}  # invert bg and fg

BASH_COLORS = {"black": "30", "red": "31", "green": "32", "yellow": "33",
               "blue": "34", "purple": "35", "cyan": "36", "white": "37"}

BASH_BGCOLORS = {"black": "40", "red": "41", "green": "42", "yellow": "43",
                 "blue": "44", "purple": "45", "cyan": "46", "white": "47"}


def _main():
    header = color("white &black")
    print

    print header + "       " + "Colors and backgrounds:      " + color()
    for c in _keys_sorted_by_values(BASH_COLORS):
        c1 = color(c)
        c2 = color(("white" if c != "white" else "black") + " &" + c)
        print c.ljust(9),
        print c1 + "colored text" + color() + "   ",
        print c2 + "background" + color()
    print

    print header + "            " + "Attributes:             " + color()
    for c in _keys_sorted_by_values(BASH_ATTRIBUTES):
        c1 = color("red " + c)
        c2 = color("white " + c)
        print c.ljust(12),
        print c1 + "red text" + color() + "    ",
        print c2 + "white text" + color()
    print
    return


def color(params=""):
    if not is_bash():
        return ""

    ret = "\x1b[0"
    for param in params.lower().split():
        if param in BASH_ATTRIBUTES:
            ret += ";" + BASH_ATTRIBUTES[param]
        elif param in BASH_COLORS:
            ret += ";" + BASH_COLORS[param]
        elif param[0] == "&" and param[1:] in BASH_BGCOLORS:
            ret += ";" + BASH_BGCOLORS[param[1:]]
        else:
            raise ValueError("Unknown param: " + param)
    return ret + "m"


def is_bash():
    return os.environ.get("SHELL", "unknown").endswith("bash")


def _keys_sorted_by_values(adict):
    """Return list of the keys of @adict sorted by values."""
    return sorted(adict.keys(), lambda x, y: cmp(adict[x], adict[y]))


if __name__ == "__main__":
    _main()
