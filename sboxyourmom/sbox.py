import re
import numpy as np
from functools import lru_cache
from sboxyourmom.hadamard import *

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

    @lru_cache()
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

    @lru_cache()
    def difference_distribution_table(self):
        nrows = 1 << self.m
        ncols = 1 << self.n

        A = [[0] * ncols for _ in range(nrows)]
        for i in range(nrows):
            si = self.S_list[i]
            for di in range(nrows):
                A[di][si^self.S_list[i^di]] += 1

        return A

    @lru_cache()
    def autocorrelation_table(self):
        ddt = np.matrix(self.difference_distribution_table())
        had = hadamard_matrix(self.n)
        A = ddt * had
        return A.tolist()

    @lru_cache()
    def linear_structures(self):
        n = self.n
        m = self.m
        act = self.autocorrelation_table()
        ret = []
        for j in range(1, 1 << n):
            for i in range(1, 1 << m):
                if abs(act[i][j]) == (1 << m):
                    c = ((1 - (act[i][j] >> m)) >> 1)
                    ret.append((j, i, c))

        return ret

    @lru_cache()
    def is_linear(self):
        LAT = self.linear_approximation_table()
        nrows = 1 << self.m
        ncols = 1 << self.n

        for y in range(nrows):
            for x in range(ncols):
                if LAT[y][x] not in (LAT[0][0], 0):
                    return False

        return True

    @lru_cache()
    def is_affine(self):
        LAT = self.linear_approximation_table()
        nrows = 1 << self.m
        ncols = 1 << self.n

        for y in range(nrows):
            for x in range(ncols):
                if abs(LAT[y][x]) not in (LAT[0][0], 0):
                    return False

        return True


    @lru_cache()
    def matrix_equivalent(self):
        if not self.is_linear():
            return None

        LAT = self.linear_approximation_table()
        M = []
        for bit in range(self.n):
            col = 1 << bit
            row = 0
            while LAT[row][col] == 0:
                row += 1
            binary_vector = [
                (row >> x) & 1 for x in range(self.m)
            ]
            M.append(binary_vector)

        return M

    @lru_cache()
    def affine_equivalent(self):
        if not self.is_affine():
            return None

        LAT = self.linear_approximation_table()
        A = []
        B = []
        for bit in range(self.n):
            col = 1 << bit
            row = 0
            while LAT[row][col] == 0:
                row += 1

            binary_vector = [
                (row >> x) & 1 for x in range(self.m)
            ]
            A.append(binary_vector)

            if LAT[row][col] > 0:
                B.append([0])
            else:
                B.append([1])

        return A, B
