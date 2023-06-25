import re

def walsh_spectrum(array):
    """
    In-place Fast Walsh-Hadamard Transform of array
    """
    h = 1
    n = len(array)
    while h < n:
        for i in range(0, n, h*2):
            for j in range(i, i+h):
                x = array[j]
                y = array[j+h]
                array[j]   = x+y
                array[j+h] = x-y
        h *= 2

class SBox:
    def __init__(self, *args):

        if len(args) == 1:
            S = list(args[0])
        else:
            S = list(args)

        self.m = (len(S)-1).bit_length()
        self.n = max(S).bit_length()
        self.S_list = S

    def __call__(self, x):
        return self.S_list[x]

    def __getitem__(self, x):
        return self(x)

    @classmethod
    def from_file(cls, filename, sep=' |,|;|\t|\r|\n', base=None):

        with open(filename, 'r') as file:
            array = re.split(sep, file.read().lower())
            array = list(filter(lambda x: x != '', array))

        if base is None:
            if any(x in 'abcdef' for y in array for x in y):
                base = 16
            elif any(x in '23456789' for y in array for x in y):
                base = 10
            else:
                base = 2

        array = map(lambda x: int(x, base), array)
        return cls(array)


    def linear_approximation_table(self):
        nrows = 1 << self.m
        ncols = 1 << self.n

        A = [[None] * ncols for _ in range(nrows)]
        for i in range(ncols):
            row = []
            for j in range(nrows):
                row.append(1 - (((i & self.S_list[j]).bit_count() & 1)*2))
            walsh_spectrum(row)
            for j in range(nrows):
                A[j][i] = row[j] // 2

        return A

    def difference_distribution_table(self):
        nrows = 1 << self.m
        ncols = 1 << self.n

        A = [[0] * ncols for _ in range(nrows)]
        for i in range(nrows):
            si = self.S_list[i]
            for di in range(nrows):
                A[di][si^self.S_list[i^di]] += 1

        return A
