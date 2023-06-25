import argparse
import sbox

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

for sbox_file in args.input_files:
    print(sbox_file, '\n')
    S = sbox.SBox.from_file(sbox_file)
    if args.lat:
        print("Linear Approximation Table:")
        for line in S.linear_approximation_table():
            print(*line)
        print()
    if args.ddt:
        print("Difference Distribution Table:")
        for line in S.difference_distribution_table():
            print(*line)
        print()
