# SBoxYourMom

SBoxYourMom is an open-source SBox analysis utility
written in Python.
It provides a set of commands to automatically analyze
substitution boxes (SBoxes), mainly used in cryptography.
The utility aims to assist in reverse engineering SBoxes
by computing various tables and providing relevant
information.

## Features

- Compute the Linear Approximation Table (LAT) of the
  SBoxes
- Compute the Difference Distribution Table (DDT) of the
  SBoxes
- Compute the Autocorrelation Table (ACT) of the SBoxes
- Perform automatic analysis of the SBoxes

## Installation

```shell
git clone https://github.com/PoustouFlan/SBoxYourMom.git
cd SBoxYourMom
pip install -r requirements.txt
```

## Usage

The utility can be used by running the `main.py`
script with appropriate command-line arguments.
Here are the available options:

```shell
usage: main.py [-h] -in [INPUT_FILES ...] [-lat] [-ddt]
               [-act] [-auto] [-format {ansi,csv,png}]
               [-out OUTPUT]
```

- `-in path/to/your/sboxes`: specify the SBoxes to
  analyze.
  The files should contain only the integers representing
  the corresponding SBox, in either binary, decimal or
  hexadecimal form.
- `-lat`: use this option to display the Linear
  Approximation Table of all the SBoxes
- `-ddt`: use this option to display the Difference
  Distribution Table of all the SBoxes
- `-act`: use this option to display the Autocorrelation
  Table of all the SBoxes
- `-format {ansi, csv, png}`: use this option to specify
  the format of the table to be displayed.
- `-out path/to/folder`: use this option to specify
  the output folder for the tables. If not specified,
  everything is printed on standard output.
- `-auto`: use this option to perform an automatic
  analysis of all the SBoxes. It will display any relevant
  information.

## Examples

Many example SBoxes can be found in the `examples` folder.
You can add your own SBox using a similar format.

```shell
$ python main.py -in examples/He2002 -ddt -format csv
16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,2,0,0,0,2,0,2,4,0,4,2,0,0,
0,0,0,2,0,6,2,2,0,2,0,0,0,0,2,0,
0,0,2,0,2,0,0,0,0,4,2,0,2,0,0,4,
0,0,0,2,0,0,6,0,0,2,0,4,2,0,0,0,
0,4,0,0,0,2,2,0,0,0,4,0,2,0,0,2,
0,0,0,4,0,4,0,0,0,0,0,0,2,2,2,2,
0,0,2,2,2,0,2,0,0,2,2,0,0,0,0,4,
0,0,0,0,0,0,2,2,0,0,0,4,0,4,2,2,
0,2,0,0,2,0,0,4,2,0,2,2,2,0,0,0,
0,2,2,0,0,0,0,0,6,0,0,2,0,0,4,0,
0,0,8,0,0,2,0,2,0,0,0,0,0,2,0,2,
0,2,0,0,2,2,2,0,0,0,0,2,0,6,0,0,
0,4,0,0,0,0,0,4,2,0,2,0,2,0,2,0,
0,0,2,4,2,0,0,0,6,0,0,0,0,0,2,0,
0,2,0,0,6,0,0,0,0,4,0,2,0,0,2,0,

$ python main.py -in examples/affine -auto
Automatic analysis.
SBox is affine! It is equivalent to the following matrices A, B:
0 0 0 1 0 1 0 0       0
1 0 0 1 1 1 1 0       1
0 1 0 0 1 1 1 1       0
1 0 1 1 0 0 1 1       1
0 1 0 0 1 1 0 1       0
1 0 1 0 0 1 1 0       1
0 1 0 1 0 0 1 1       0
0 0 1 0 1 0 0 1       0
That is, SBox(x) = A·x ⊕ B for all x. (x represented as a column binary vector)
```

## License

SBoxYourMom is released under the MIT License

## Contributing

Contributions are welcome!
If you encounter any issues or have suggestions for
improvement, please open an issue or submit a pull
request.
