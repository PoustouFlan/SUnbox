#!/usr/bin/env python

import argparse
import os
from PIL import Image
from sys import stderr

from sboxyourmom.sbox import SBox

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

def table_to_csv(table):
    result = ''
    for y, line in enumerate(table):
        for x, elt in enumerate(line):
            result += str(elt) + ','

        result += '\n'
    return result

def table_to_ansi(table):
    red    = "\u001b[48;5;9m\u001b[38;5;15m"
    yellow = "\u001b[48;5;3m\u001b[38;5;0m"
    green  = "\u001b[48;5;10m\u001b[38;5;0m"
    green2 = "\u001b[48;5;2m\u001b[38;5;0m"
    end    = "\u001b[0m"

    upper = max(max(line) for line in table[1:])
    size = len(str(upper)) + 2

    result = ''
    for y, line in enumerate(table):
        for x, elt in enumerate(line):
            if elt == 0 or x == 0 or y == 0:
                result += green
            elif abs(elt) == 2:
                result += green2
            elif abs(elt) == upper:
                result += red
            else:
                result += yellow
            result += str(elt).rjust(size)
            result += end
        result += '\n'
    return result

def table_to_png(table):
    red    = (255, 0, 0),
    green  = (0, 255, 0),
    green2 = (22, 222, 22),
    yellow = (255, 255, 0),

    #upper = max(max(line) for line in table[1:])
    upper = table[0][0]
    size = len(str(upper)) + 2

    width = len(table[0])
    height = len(table)

    image = Image.new("RGB", (width, height))

    for y, line in enumerate(table):
        for x, elt in enumerate(line):
            if elt == 0 or x == 0 or y == 0:
                color = green
            elif abs(elt) == 2:
                color = green2
            elif abs(elt) == upper:
                color = red
            else:
                ratio = 1 - (abs(elt) - 4) / (upper - 4)
                color = (255, int(255*ratio), 0)
            image.putpixel((x, y), color)

    return image

def print_table(table, format='ansi', filename='stdout'):
    if format == 'ansi':
        output = table_to_ansi(table)
    elif format == 'csv':
        output = table_to_csv(table)
    elif format == 'png':
        output = table_to_png(table)

    if filename == 'stdout':
        if format == 'png':
            print(output.tobytes().hex())
        else:
            print(output)
    elif format == 'png':
        output.save(filename, "png")
    else:
        with open(filename, 'w') as file:
            file.write(output)

for sbox_file in args.input_files:
    debug(sbox_file, '\n')
    S = SBox.from_file(sbox_file)

    if args.auto:
        debug("Automatic analysis.")
        if S.is_linear():
            debug("SBox is linear! It is equivalent to the following matrix M:")
            for line in S.matrix_equivalent():
                print(*line)
            debug("That is, SBox(x) = M·x for all x. "
                  "(x represented as a column binary vector)")
        elif S.is_affine():
            debug("SBox is affine! It is equivalent to the following matrices A, B:")
            A, B = S.affine_equivalent()
            for y in range(S.n):
                print(*A[y], ' \t ', B[y][0])
            debug("That is, SBox(x) = A·x + B for all x. "
                  "(x represented as a column binary vector)")
        else:
            debug("SBox is not linear.")
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
