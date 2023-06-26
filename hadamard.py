import numpy as np

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

def hadamard_matrix(n):
    """
    Generates a hadamard matrix of size 2^n
    """
    if n == 0:
        return np.array([[1]])
    else:
        h_n_minus_1 = hadamard_matrix(n - 1)
        h_n = np.vstack(
            (np.hstack((h_n_minus_1,  h_n_minus_1)),
             np.hstack((h_n_minus_1, -h_n_minus_1)))
        )
        return h_n
