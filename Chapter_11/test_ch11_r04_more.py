"""Python Cookbook 2nd ed.

Chapter 11, recipe 4 and 5. Unit testing with the unittest module, Combining Unittest and Doctest.

A more conventional name would be test_ch11_r04.py
"""
import doctest

import Chapter_11.ch11_r01 as ch11_r01
import Chapter_11.ch11_r08 as ch11_r08
import Chapter_11.ch11_r09 as ch11_r09

# Chapter 3's test_point example has a repr() problem
# The test needs rework to fit this pattern.
import Chapter_11.ch11_r03 as ch11_r03


def load_tests(loader, standard_tests, pattern):
    for module in (
        ch11_r01, ch11_r08, ch11_r09
    ):
        dt = doctest.DocTestSuite(module)
        standard_tests.addTests(dt)
    return standard_tests
