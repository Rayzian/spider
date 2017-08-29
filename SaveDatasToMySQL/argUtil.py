#! usr/bin/python
# -*- coding: utf-8 -*-

import argparse


def genParserClient():
    description = "usage: % prog[options] poetry - file"

    parser = argparse.ArgumentParser('Usage: %prog [options] arg1 arg2 ...')


    parser.add_argument('-s', action='store',

                        dest='simple_value',

                        help='Storea simple value')

    parser.add_argument('-c', action='store_const',

                        dest='constant_value',

                        const='value-to-store',

                        help='Store a constant value')

    parser.add_argument('-t', action='store_true',

                        default=False,

                        dest='boolean_switch',

                        help='Set a switch to true')

    parser.add_argument('-f', action='store_false',

                        default=False,

                        dest='boolean_switch',

                        help='Set a switch to false')

    parser.add_argument('-a', action='append',

                        dest='collection',

                        default=[],

                        help='Add repeated values to a list')

    parser.add_argument('-A', action='append_const',

                        dest='const_collection',

                        const='value-1-to-append',

                        default=[],

                        help='Add different values to list')

    parser.add_argument('-B', action='append_const',

                        dest='const_collection',

                        const='value-2-to-append',

                        help='Add different values to list')

    parser.add_argument('--version', action='version',

                        version='%(prog)s 1.0')

    return parser.parse_args()
