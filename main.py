import argparse
import sbox

red    = "\u001b[48;5;9m\u001b[38;5;15m"
yellow = "\u001b[48;5;3m\u001b[38;5;0m"
green  = "\u001b[48;5;10m\u001b[38;5;0m"
green2 = "\u001b[48;5;2m\u001b[38;5;0m"
end    = "\u001b[0m"

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

args = parser.parse_args()

def print_table(lat):
    upper = max(max(line) for line in lat[1:])
    size = len(str(upper)) + 2

    for y, line in enumerate(lat):
        for x, elt in enumerate(line):
            if elt == 0 or (x, y) == (0, 0):
                print(green, end = '')
            elif abs(elt) == 2:
                print(green2, end = '')
            elif abs(elt) == upper:
                print(red, end = '')
            else:
                print(yellow, end = '')
            print(str(elt).rjust(size), end = end)
        print()


for sbox_file in args.input_files:
    print(sbox_file, '\n')
    S = sbox.SBox.from_file(sbox_file)
    if args.lat:
        print("Linear Approximation Table:")
        print_table(S.linear_approximation_table())
        print()

    if args.ddt:
        print("Difference Distribution Table:")
        print_table(S.difference_distribution_table())
        print()
