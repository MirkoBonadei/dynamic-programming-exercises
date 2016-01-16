"""Making change problem.

How can a given amount of money be made with the least number of coins of given 
value? 
WARNING: There must be a coin with value equal to 1 to ensure that a solution 
exists.
"""

import unittest
import sys
import copy

class CashRegister(object):

    # TODO: bottom up solution

    def make_change_memoized(self, amount, coins):
        memo = {0: [0] * len(coins)}
        return self._make_change_memoized(amount, coins, memo)

    def _make_change_memoized(self, amount, coins, memo):
        if amount in memo:
            return memo[amount]
        else:
            min_solution = [0] * len(coins)
            # I can always reach a solution using the minimum currency
            # (see problem definition)
            min_solution[0] = amount
            for coin_index in range(0, len(coins)):
                if (amount - coins[coin_index]) >= 0:
                    subproblem_amount = amount - coins[coin_index]
                    subproblem_solution = self._make_change_memoized(subproblem_amount,
                                                                     coins, 
                                                                     memo)
                    if self._count_coins(min_solution) > self._count_coins(subproblem_solution) + 1:
                        min_solution = copy.deepcopy(subproblem_solution)
                        min_solution[coin_index] += 1
                        memo[amount] = min_solution
            return min_solution

    def _count_coins(self, coin_count_by_currency):
        total = 0
        for counter in coin_count_by_currency:
            total += counter
        return total

class CashRegisterTest(unittest.TestCase):

    def setUp(self):
        self.cash_register = CashRegister()

    def test_simple_problems(self):
        self.assertEqual([1, 0, 3],
                         self.cash_register.make_change_memoized(10, 
                                                                 [1, 2, 3]))
        self.assertEqual([0, 0, 0, 0, 0, 0, 0, 1],
                         self.cash_register.make_change_memoized(100, 
                                                                 [1, 2, 5, 10, 
                                                                  15, 20, 50, 
                                                                  100]))
        self.assertEqual([0, 1, 1],
                         self.cash_register.make_change_memoized(5, 
                                                                 [1, 2, 3]))

if __name__ == "__main__":
    unittest.main()
