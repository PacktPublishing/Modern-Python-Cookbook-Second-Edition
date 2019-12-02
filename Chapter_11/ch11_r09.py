"""Python Cookbook 2nd ed.

Chapter 11, recipe 9. Random.
"""


import random


def resample(population, N):
    for i in range(N):
        sample = random.choice(population)
        yield sample
