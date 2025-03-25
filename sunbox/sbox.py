import re
import numpy as np
import heapq
from functools import lru_cache
from sunbox.hadamard import *

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

    def __xor__(self, k):
        return SBox(x ^ k for x in self.S_list)

    def __mul__(self, k):
        return SBox((x * k) % (1 << self.n) for x in self.S_list)

    def rotl(self, k):
        return SBox(
            ((x << k) | (x >> (self.n - k))) % (1 << self.n)
            for x in self.S_list
        )

    @classmethod
    def from_file(cls, filename, sep=' |,|;|\t|\r|\n', base=None):
        """
        Reads a SBox from a file.
        If the base is not specified, it is automatically detected.
        """
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
        """
        Returns the Linear Approximation Table (LAT) for this SBox.
        LAT[a][b] corresponds to the probability P[a·x = b·S(x)],
        where · denotes a vector dot product.

        Absolute bias scale is used, therefore the actual value
        corresponds to the probability - 1/2, multiplied by 2^m.
        """
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
        """
        Returns the Difference Distribution Table (DDT) for this SBox.
        DDT[a][b] corresponds to the probability P[S(x⊕a) = S(x)⊕b].

        Values are multiplied by 2^m to remain integers.
        """
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
        """
        Returns the Autocorrelation Table (ACT) for this SBox.
        ACT[a][b] corresponds to the probability P[b·(S(x)⊕S(x⊕a)) = 0],
        where · denotes a vector dot product.

        Absolute bias scale is used, therefore the actual value
        corresponds to the probability - 1/2, multiplied by 2^m.
        """
        ddt = np.matrix(self.difference_distribution_table())
        had = hadamard_matrix(self.n)
        A = ddt * had
        return A.tolist()

    @lru_cache()
    def linear_structures(self):
        """
        Returns a list of all three-tuples (b,a,c) (a,b ≥ 1) such that
        b·(S(x)⊕S(x⊕a)) = c for all x, where · denotes a vector dot
        product.
        """
        n = self.n
        m = self.m
        act = self.autocorrelation_table()
        ret = []
        for b in range(1, 1 << n):
            for a in range(1, 1 << m):
                if abs(act[a][b]) == (1 << m):
                    c = ((1 - (act[a][b] >> m)) >> 1)
                    ret.append((b, a, c))

        return ret

    @lru_cache()
    def is_linear(self):
        """
        Checks whether S(x) is a linear transformation,
        that is, there exists a binary matrix M such that S(x) = M·x,
        where x is expressed as a column binary vector.
        """
        LAT = self.linear_approximation_table()
        nrows = 1 << self.m
        ncols = 1 << self.n

        for y in range(nrows):
            for x in range(ncols):
                if LAT[y][x] not in (LAT[0][0], 0):
                    return False

        return True

    @lru_cache()
    def is_xor(self):
        """
        Checks whether S(x) is a simple XOR function,
        that is, there exists an integer k such that S(x) = x ⊕ k.
        """
        k = self.S_list[0]
        for i, y in enumerate(self.S_list):
            if y != k ^ i:
                return False
        return True

    @lru_cache()
    def is_affine(self):
        """
        Checks whether S(x) is an affine transformation,
        that is, there exists a binary matrix A and a binary
        column vector b such that S(x) = A·x ⊕ b,
        where x is expressed as a column binary vector.
        """
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
        """
        If it exists, returns the binary matrix M such that S(x) = M·x,
        where x is expressed as a column binary vector.
        """

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
        """
        If they exists, returns a binary matrix A and a binary
        column vector b such that S(x) = A·x ⊕ b,
        where x is expressed as a column binary vector.
        """

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

    @lru_cache()
    def maximal_linear_bias(self):
        """
        Returns all linear approximations that appears with maximal
        probability and the corresponding probability.

        The first element returned is the probability p,
        then a list of three-tuples (a, b, c), meaning that
        a·x = b·S(x)⊕c with probability p, where · denotes a vector
        dot product.
        """
        nrows = 1 << self.m
        ncols = 1 << self.n

        maximal_bias = 0
        linear_approximations = []

        LAT = self.linear_approximation_table()

        for y in range(1, ncols):
            for x in range(1, nrows):
                if abs(LAT[y][x]) > maximal_bias:
                    maximal_bias = abs(LAT[y][x])
                    linear_approximations = []

                if abs(LAT[y][x]) >= maximal_bias:
                    c = 0 if LAT[y][x] > 0 else 1
                    linear_approximations.append((y, x, c))

        probability = (maximal_bias / nrows) + 0.5
        return probability, linear_approximations

    @lru_cache()
    def is_differential(self):
        """
        Checks whether S(x)⊕b = S(x⊕a) for some a, b.
        """
        nrows = 1 << self.m
        ncols = 1 << self.n

        DDT = self.difference_distribution_table()

        for y in range(ncols):
            for x in range(nrows):
                if (x, y) == (0, 0):
                    continue
                if DDT[y][x] == DDT[0][0]:
                    return True
        return False

    @lru_cache()
    def is_bijective(self):
        """
        Checks whether the SBox is bijective.
        """
        if self.m != self.n:
            return False
        expected_range = set(range(2**self.m))
        return set(self.S_list) == expected_range

    @lru_cache()
    def maximal_differential_bias(self):
        """
        Returns all differential approximations that appears with maximal
        probability and the corresponding probability.

        The first element returned is the probability p,
        then a list of two-tuples (a, b), meaning that
        S(x)⊕b = S(x⊕a) with probability p.
        """
        nrows = 1 << self.m
        ncols = 1 << self.n

        maximal_bias = 0
        differential_approximations = []

        DDT = self.difference_distribution_table()

        for y in range(0, ncols):
            for x in range(0, nrows):
                if (x, y) == (0, 0):
                    continue
                if DDT[y][x] > maximal_bias:
                    maximal_bias = DDT[y][x]
                    differential_approximations = []

                if DDT[y][x] >= maximal_bias:
                    differential_approximations.append((y, x))

        probability = (maximal_bias / nrows)
        return probability, differential_approximations

    @lru_cache()
    def biryukov_perrin_metric(self):
        """
        Implements a "distance to identity" metric based on the DDT:
        M(s) = Σl≥2 Nl(l−2)², where Nl counts coefficients with value
        l in the DDT of the SBox.
        """
        nrows = 1 << self.m
        ncols = 1 << self.n

        DDT = self.difference_distribution_table()
        distance = 0

        for y in range(1, ncols):
            for x in range(1, nrows):
                if DDT[y][x] > 2:
                    distance += (DDT[y][x] - 2) ** 2

        return distance

    def break_arithmetic(self):
        """
        TODO
        """
        target = ((1 << self.m)-2)**2 * ((1 << self.m)-1)
        heap = [(target - self.biryukov_perrin_metric(), "S", self)]

        t = 0
        while True:
            metric, name, sbox = heapq.heappop(heap)
            for k in range(1 << self.m):
                print(k)
                sbox2 = sbox ^ k
                for r in range(self.m):
                    sbox3 = sbox2.rotl(r)
                    for i in range(1 << (self.m-1)):
                        m = i*2+1
                        sbox4 = sbox3 * m
                        heapq.heappush(heap, (
                            target - sbox4.biryukov_perrin_metric(),
                            f"{name}⊕{k}<<<{r}·{m}",
                            sbox4
                        ))
            break
        print(heap[0])
