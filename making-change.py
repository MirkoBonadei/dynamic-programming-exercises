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

    # Dynamic programming solution

    def make_change_dp(self, amount, coin_values):
        """Dynamic programming solution.

        We build two 1xamount tables to keep trace of the minimum number 
        of coins needed and the next coin to include in the change.

        Args:
        - amount (int): the amount to change
        - coin_values (list): the list of possible coin values (the value 1 must
                              be included)

        Returns:
        tuple: (number of coins, list of coins)
        """
        number_of_coins_list = [0] * (amount + 1)
        next_coin_list = [0] * (amount + 1)

        for amount_tmp in range(0, amount + 1):
            number_of_coins = amount_tmp # using only coins of value 1
            next_coin = 1
            for value in coin_values:
                if value <= amount_tmp:
                    if number_of_coins_list[amount_tmp - value] + 1 < number_of_coins:
                        number_of_coins = number_of_coins_list[amount_tmp - value] + 1
                        next_coin = value
            number_of_coins_list[amount_tmp] = number_of_coins
            next_coin_list[amount_tmp] = next_coin
        return (number_of_coins_list[amount], 
                self._list_of_coins_to_reach_amount(next_coin_list, amount))

    def _list_of_coins_to_reach_amount(self, next_coin, amount):
        amount_tmp = amount
        list_of_coins = []
        while amount_tmp > 0:
            list_of_coins.append(next_coin[amount_tmp])
            amount_tmp = amount_tmp - next_coin[amount_tmp]
        list_of_coins.reverse()
        return list_of_coins

    # Memoized solution

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

    def test_dynamic_programming_solution(self):
        expected = (4, [3, 3, 3, 1]) # (number of coins, values)
        actual = self.cash_register.make_change_dp(10, [1, 2, 3])
        self.assertEqual(expected, actual)

    def test_dynamic_programming_solution_with_a_difficult_problem_for_greedy_algorithms(self):
        expected = (3, [21, 21, 21])
        actual = self.cash_register.make_change_dp(63, [1, 5, 10, 21, 25])
        self.assertEqual(expected, actual)

    def test_dynamic_programming_solution_with_long_problem(self):
        expected = (1, [100])
        actual = self.cash_register.make_change_dp(100, [1, 2, 5, 10, 
                                                         15, 20, 50, 100])
        self.assertEqual(expected, actual)

    def test_simple_problems_for_memoized_solution(self):
        self.assertEqual([1, 0, 3],
                         self.cash_register.make_change_memoized(10, 
                                                                 [1, 2, 3]))
        self.assertEqual([0, 0, 0, 3, 0],
                         self.cash_register.make_change_memoized(63,
                                                                 [1, 5, 10, 21, 25]))
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
