#!/usr/bin/env python

import argparse
import os
from sys import stderr

from sunbox.sbox import SBox
from sunbox.format import *

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
    '-output', '-out',
    default = 'stdout',
    help = 'Output directory path or "stdout" to print to standard output'
)

args = parser.parse_args()


for sbox_file in args.input_files:
    debug(sbox_file, '\n')
    S = SBox.from_file(sbox_file)

    if args.auto:
        debug("Automatic analysis.")

        # Linear cryptanalysis
        if not S.is_bijective():
                    print("Warning: The SBox is not bijective.")
        if S.is_linear():
            print("SBox is linear! It is equivalent to the following matrix M:")
            for line in S.matrix_equivalent():
                print(*line)
            print("That is, SBox(x) = M·x for all x. "
                  "(x represented as a column binary vector)")
        elif S.is_xor():
            print("SBox is a simple XOR! It is equivalent to the following equation:")
            print(f"    S(x) = x ⊕ {S[0]}")
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
            if p >= 0.6:
                print(f"However, these equations hold with probability {round(100*p, 2)}%:")
                for a, b, c in approximations:
                    print(
                        ' ',
                        to_polynomial(b, 'y'),
                        '=',
                        to_polynomial(a, 'x'),
                        '⊕ 1' if c == 1 else ''
                    )
                print("where y = S(x).")
            if p >= 0.75:
                print("This can be considered as a cryptographic weakness and can lead to linear cryptanalysis.")


            # Differential cryptanalysis
            print()
            if S.is_differential():
                p, approximations = S.maximal_differential_bias()
                print("SBox is differential! For all x,")
                for a, b in approximations:
                    if b == 0:
                        print(f"  S(x) = S(x⊕{a})")
                    else:
                        print(f"  S(x)⊕{b} = S(x⊕{a})")
                print()
            else:
                p, approximations = S.maximal_differential_bias()
                if p >= 0.1:
                    print(f"These equations hold with probability {round(100*p, 2)}%:")
                    for a, b in approximations:
                        print(f"S(x)⊕{b} = S(x⊕{a})")
                    print("This can be considered as a cryptographic weakness and can lead to differential cryptanalysis.")

                # Linear structures
                print()
                linear_structures = S.linear_structures()
                if len(linear_structures) > 0:
                    print("The SBox has linear structures! "
                          "For all x,")
                    for b, a, c in linear_structures:
                        print(f"  {b}·(S(x)⊕S(x⊕{a})) = {c}")
                    print("where · denotes a vector dot product.")

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
