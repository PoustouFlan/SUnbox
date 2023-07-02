#!/usr/bin/env python

import argparse
import os
from PIL import Image
from sys import stderr

from sboxyourmom.sbox import SBox
from sboxyourmom.format import *

def debug(*args, **kwargs):
    print(*args, **kwargs, file = stderr, flush = True)

parser = argparse.ArgumentParser(
    description = "An open-source SBox analysis utility",
)

parser.add_argument(
    '-in', '-i',
    dest = 'input_files',
    required = True,
    nargs = '*',
    help = 'Input file(s) containing the SBoxes to analyze'
)

parser.add_argument(
    '-lat',
    action = 'store_true',
    help = 'Compute the Linear Approximation Table of the SBoxes'
)

parser.add_argument(
    '-ddt',
    action = 'store_true',
    help = 'Compute the Difference Distribution Table of the SBoxes'
)

parser.add_argument(
    '-act',
    action = 'store_true',
    help = 'Compute the Autocorrelation Table of the SBoxes'
)

parser.add_argument(
    '-auto',
    action = 'store_true',
    help = 'Performs an automatic analysis of the SBoxes and outputs relevant information'
)

parser.add_argument(
    '-format',
    choices = ['ansi', 'csv', 'png'],
    default = 'ansi',
    help = 'Output format for the tables',
)

parser.add_argument(
    '-output',
    default = 'stdout',
    help = 'Output directory path or "stdout" to print to standard output'
)

args = parser.parse_args()


for sbox_file in args.input_files:
    debug(sbox_file, '\n')
    S = SBox.from_file(sbox_file)

    if args.auto:
        debug("Automatic analysis.")
        if S.is_linear():
            print("SBox is linear! It is equivalent to the following matrix M:")
            for line in S.matrix_equivalent():
                print(*line)
            print("That is, SBox(x) = M·x for all x. "
                  "(x represented as a column binary vector)")
        elif S.is_affine():
            print("SBox is affine! It is equivalent to the following matrices A, B:")
            A, B = S.affine_equivalent()
            for y in range(S.n):
                print(*A[y], ' \t ', B[y][0])
            print("That is, SBox(x) = A·x ⊕ B for all x. "
                  "(x represented as a column binary vector)")
        else:
            print("SBox is not linear.")
            p, approximations = S.maximal_linear_bias()
            print(f"However, these equations hold with probability {round(100*p, 2)}%:")
            for a, b, c in approximations:
                print(
                    to_polynomial(a, 'x'),
                    '=',
                    to_polynomial(b, 'y'),
                    '⊕ 1' if c == 1 else ''
                )
            print("where y = S(x).")

    #debug("Linear structures:")
    #debug(S.linear_structures())

    if args.lat:
        debug("Linear Approximation Table")
        table = S.linear_approximation_table()
        format = args.format
        if args.output == 'stdout':
            filename = 'stdout'
        else:
            filename = os.path.splitext(os.path.basename(sbox_file))[0]
            filename = os.path.join(
                args.output,
                f"lat_{filename}.{format}"
            )
        print_table(table, format, filename)
        debug()

    if args.ddt:
        debug("Difference Distribution Table")
        table = S.difference_distribution_table()
        format = args.format
        if args.output == 'stdout':
            filename = 'stdout'
        else:
            filename = os.path.splitext(os.path.basename(sbox_file))[0]
            filename = os.path.join(
                args.output,
                f"ddt_{filename}.{format}"
            )
        print_table(table, format, filename)
        debug()

    if args.act:
        debug("Autocorrelation Table")
        table = S.autocorrelation_table()
        format = args.format
        if args.output == 'stdout':
            filename = 'stdout'
        else:
            filename = os.path.splitext(os.path.basename(sbox_file))[0]
            filename = os.path.join(
                args.output,
                f"act_{filename}.{format}"
            )
        print_table(table, format, filename)
        debug()
