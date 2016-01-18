"""Longest Common Subsequence Problem.

Given two sequences X and Y , we say that a sequence Z is a common 
subsequence of X and Y if Z is a subsequence of both X and Y. 

For example, if X = [A, B, C, B, D, A, B] and Y = [B, D, C, A, B, A], 
the sequence [B, C, A] is a common subsequence of both X and Y. 
The sequence [B, C, A] is not a longest common subsequence (LCS) of X and Y, 
however, since it has length 3 and the sequence [B, C, B, A], which is also 
common to both X and Y, has length 4. 
The sequence [B, C, B, A] is an LCS of X and Y, as is the sequence [B, D, A, B],
since X and Y have no common subsequence of length 5 or greater.
In the longest-common-subsequence problem, we are given two sequences
X and Y and wish to find a maximum-length common subsequence of X and Y.
"""

import unittest

class LongestCommonSubsequence(object):

    def lcs_length(self, s1, s2):
        table = []
        for row_id in range(0, len(s1) + 1):
            table.append([0] * (len(s2) + 1))
        for s1_id in range(0, len(s1)):
            for s2_id in range(0, len(s2)):
                row_id = s1_id + 1
                column_id = s2_id + 1
                if s1[s1_id] == s2[s2_id]:
                    table[row_id][column_id] = table[row_id-1][column_id-1] + 1
                else:
                    table[row_id][column_id] = max(table[row_id-1][column_id], 
                                                   table[row_id][column_id-1])
        return table[len(s1)][len(s2)]

class LongestCommonSubsequenceTest(unittest.TestCase):

    def setUp(self):
        self.lcs = LongestCommonSubsequence()

    def test_simple_subsequence_length(self):
        s1 = "ABCBDAB"
        s2 = "BDCABA"
        expected_length = 4
        actual_length = self.lcs.lcs_length(s1, s2)
        self.assertEqual(expected_length, actual_length)

    def test_no_common_subsequence_means_0_length(self):
        self.assertEqual(0, self.lcs.lcs_length("ABC", "DEF"))

    def test_lcs_from_clrs(self):
        # Chapter 15.4 of CLRS
        s1 = "ACCGGTCGAGTGCGCGGAAGCCGGCCGAA"
        s2 = "GTCGTTCGGAATGCCGTTGCTCTGTAAA"
        expected_length = 20
        actual_length = self.lcs.lcs_length(s1, s2)
        self.assertEqual(expected_length, actual_length)

if __name__ == "__main__":
    unittest.main()
