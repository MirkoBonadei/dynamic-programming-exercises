"""The rod cutting problem.

This problem is taken from the chapter 15.1 of the book 
"Introduction to Algorithms and Data Structures" (CLRS).

The rod-cutting problem is the following: 
Given a rod of length n inches and a table of prices p[i] for i D 1, 2, ..., n, 
determine the maximum revenue r[n] obtainable by cutting up the rod and selling 
the pieces. 
Note that if the price p[n] for a rod of length n is large enough, an optimal 
solution may require no cutting at all.
"""

import unittest

class RodCutter(object):

    # Bruteforce solution
    def maximize_revenue(self, rod_length, price_table):
        if rod_length == 0:
            return 0
        max_revenue = 0
        for cut_index in range(1, rod_length + 1):
            max_revenue = max(
                max_revenue,
                price_table[cut_index] + \
                self.maximize_revenue(
                    rod_length - cut_index,
                    price_table
                )
            )
        return max_revenue

    # Memoized solution
    def maximize_revenue_memoized(self, rod_length, price_table):
        # We use a dictionary to implement the memo. 
        # memo[0] = solution to the problem with rod length of 0
        # memo[n] = solution to the problem with rod length of n
        return self._maximize_revenue_memoized(
            rod_length,
            price_table,
            {0: 0}
        )

    def _maximize_revenue_memoized(self, rod_length, price_table, memo):
        if rod_length == 0:
            return 0
        if rod_length in memo:
            return memo[rod_length]
        else:
            maximized_revenue = 0
            for cut_index in range(1, rod_length + 1):
                maximized_revenue = max(
                    maximized_revenue, 
                    price_table[cut_index] + \
                    self._maximize_revenue_memoized(
                        rod_length - cut_index,
                        price_table,
                        memo
                    )
                )
            memo[rod_length] = maximized_revenue
            return maximized_revenue

    # Bottom up solution (ordering subproblems before solve them)
    def maximize_revenue_bottom_up(self, rod_length, price_table):
        max_revenues_by_rod_length = {0: 0}
        for subproblem_rod_length in range(1, rod_length + 1):
            max_revenue = 0
            for cut_index in range(1, subproblem_rod_length + 1):
                max_revenue = max(
                    max_revenue,
                    price_table[cut_index] + \
                    max_revenues_by_rod_length[subproblem_rod_length - cut_index]
                )
            max_revenues_by_rod_length[subproblem_rod_length] = max_revenue
        return max_revenues_by_rod_length[rod_length]

class RodCutterTest(unittest.TestCase):

    def setUp(self):
        self.rod_cutter = RodCutter()
        self.price_table = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]

    def testWhenThereIsNothingToCutTheMaxRevenueIsZero(self):
        self.assertEqual(
            0, 
            self.rod_cutter.maximize_revenue(0, self.price_table)
        )

    def testWhenThePriceOfTheRodIsLargeEnoughThereIsNoCut(self):
        self.assertEqual(
            5, 
            self.rod_cutter.maximize_revenue(2, self.price_table)
        )

    def testWhenTheRodLengthIsFourThenTheMaxRevenueIsTen(self):
        self.assertEqual(
            10,
            self.rod_cutter.maximize_revenue(4, self.price_table)
        )

    def testWhenTheRodLengthIsSevenThenTheMaxRevenueIsEighteen(self):
        self.assertEqual(
            18,
            self.rod_cutter.maximize_revenue(7, self.price_table)
        )

    def testWhenTheRodLengthIsTenThenTheMaxRevenueIsThirty(self):
        self.assertEqual(
            30,
            self.rod_cutter.maximize_revenue(10, self.price_table)
        )

    def testItTakesTooMuchToCompleteWithoutOptimizations(self):
        """
        The maximize_revenue algorithm has a time complexity of O(2**n).
        In the previous tests n was <= 10 and the result was achievable in 
        less than a second. But with n = 35 it takes lot of time.
        In this test we want to ensure that the algorithm is fast while 
        ensuring regression with the previous tests.
        """
        linear_price_table = []
        for rod_length in range(0, 36):
            linear_price_table.append(rod_length)
        self.assertTrue(
            # Bruteforce is too slow
            #self.rod_cutter.maximize_revenue(35, linear_price_table) > 0
            self.rod_cutter.maximize_revenue_memoized(35, linear_price_table) > 0
        )

    def testRegressionAmongDifferentImplementations(self):
        for rod_length in range(0, len(self.price_table)):
            self.assertTrue(
                self.rod_cutter.maximize_revenue(rod_length, self.price_table) == \
                self.rod_cutter.maximize_revenue_memoized(rod_length, self.price_table) == \
                self.rod_cutter.maximize_revenue_bottom_up(rod_length, self.price_table)
            )

if __name__ == "__main__":
    unittest.main()
