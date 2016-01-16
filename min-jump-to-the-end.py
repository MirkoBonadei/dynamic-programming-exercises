"""Minimum number of jumps problem.

Given an array of integers where each element represents the max number of steps
that can be made forward from that element. Write a function to return the 
minimum number of jumps to reach the end of the array (starting from the first 
element). If an element is 0, then cannot move through that element.
"""

import unittest
import sys

class PathFinder(object):

    def __init__(self):
        self.max_value = sys.maxint

    def min_jumps(self, path):
        # number of jumps to reach the ith element starting from 0
        jumps = [self.max_value] * len(path)
        jumps[0] = 0 # no jumps needed to reach the first element
        for i in range(1, len(path)):
            for j in range(0, i):
                if (i - j) <= path[j] and jumps[j] != self.max_value:
                    jumps[i] = min(1 + jumps[j], jumps[i])
        return jumps[len(path) - 1]

class PathFInderTestTest(unittest.TestCase):

    def setUp(self):
        self.path_finder = PathFinder()

    def test_first_example(self):
        path = [1, 3, 5, 8, 9, 2, 6, 7, 6, 8, 9]
        self.assertEquals(3, self.path_finder.min_jumps(path))

    def test_second_example(self):
        path = [1, 4, 3, 7, 1, 2, 6, 7, 6, 10]
        self.assertEquals(3, self.path_finder.min_jumps(path))

    def test_with_a_long_road(self):
        # I don't know the answer but it will be surely greater than 2
        # It is the running time which matters here. Without dynamic programming
        # it would take lot of time to complete.
        very_long_path = [1, 3, 5, 8, 9, 2, 6, 7,
                          6, 8, 9, 2, 3, 6, 1, 3, 
                          2, 9, 2, 3, 4, 7, 9, 3, 
                          2, 4, 5, 6, 7, 8, 9, 1, 
                          2, 3, 1, 1, 1, 1, 1 ,4,
                          5 ,6, 7, 8, 9]
        self.assertTrue(self.path_finder.min_jumps(very_long_path) > 2)
     
if __name__ == "__main__":
    unittest.main()
