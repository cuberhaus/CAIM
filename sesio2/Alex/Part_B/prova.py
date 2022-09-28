import math
import numpy as np
import numpy.linalg
import sklearn


def normalize(tw):
    """
    Normalizes the weights in t so that they form a unit-length vector
    It is assumed that not all weights are 0
    :param tw:
    :return:
    """
    sum = 0
    for i in tw:
        sum += i ** 2
    vmod = math.sqrt(sum)
    for i in range(len(tw)):
        tw[i] = tw[i] / vmod
    return None


vec = [1, 2, 3, 4]
vec2 = [1, 2, 3, 4]
normalize(vec)
print(vec)
print(vec2/np.linalg.norm(vec2))
