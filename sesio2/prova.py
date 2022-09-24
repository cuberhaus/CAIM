import math
import numpy as np
import numpy.linalg
import sklearn
from scipy.spatial import distance

from numpy import dot
from numpy.linalg import norm

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


def cosine_similarity(tw1, tw2):
    """
    Computes the cosine similarity between two weight vectors, terms are alphabetically ordered
    :param tw1:
    :param tw2:
    :return:
    """
    # res = [0] * len(tw1)
    res = 0
    normalize(tw1)
    normalize(tw2)
    for i in range(len(tw1)):
        res += tw1[i] * tw2[i]
    sum = 0
    sum2 = 0
    for i in range(len(tw1)):
        sum += tw1[i] ** 2
        sum2 += tw2[i] ** 2
    l1 = math.sqrt(sum)
    l2 = math.sqrt(sum2)

    res = res / (l1 * l2)
    return res


vec = [1, 2, 3, 4]
vec2 = [20, 2, 3, 4]
print(distance.cosine(vec, vec2))
vec = [1, 2, 3, 4]
vec2 = [20, 2, 3, 4]
print(1-cosine_similarity(vec, vec2))

# vec = [1, 2, 3, 4]
# vec2 = [1, 2, 3, 4]
# normalize(vec)
# print(vec)
# print(vec2/np.linalg.norm(vec2))
