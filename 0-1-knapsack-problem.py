"""The 0-1 Knapsack Problem.

Given a knapsack with maximum weight capacity W and a set of items numbered 
from 1 to n, each with a weight w[i] and a value v[i]: 
- Maximise the sum of the value of the objects included in the knapsack
- While keeping the total weight of the knapsack less than or equal to W
"""

import unittest

class Knapsack_0_1(object):

    def solve(self, max_weight, weights, values):
        """
        Args:
        - capacity (int): the capacity of the knapsack
        - weights (list): the list with the weights of the objects
        - values (list): the list with the values of the objects

        Returns:
        list: with the indexes of the objects included in the knapsack

        We want to build a table with the solutions of the subproblems:
        [- 0 1 2 3 4 ... n]
        [0                ]
        [1                ] 
        [2                ]
        [3               S]
        On the first row we have the capacity of the Knapsack while on the
        first column we have the items included in the problem.
        The maximum value that you can put in a Knapsack is the value S.

        To build the list with items included in the optimal solution we have
        to keep a second table with 1 in case the item is included in the 
        solution reppresented by the element of the matrix.
        """
        m = []
        k = []
        for item_id in range(0, len(weights) + 1):
            m.append([0] * (max_weight + 1))
            k.append([0] * (max_weight + 1))

        for item_id in range(0, len(weights)):
            row_id = item_id + 1
            for current_max_weight in range(0, max_weight + 1):
                value_with_item = values[item_id] + m[row_id - 1][current_max_weight - weights[item_id]]
                value_without_item = m[row_id - 1][current_max_weight]
                if weights[item_id] <= current_max_weight and value_with_item > value_without_item:
                    m[row_id][current_max_weight] = value_with_item
                    k[row_id][current_max_weight] = 1
                else:
                    m[row_id][current_max_weight] = m[row_id - 1][current_max_weight]
                    k[row_id][current_max_weight] = 0
        # building the solution
        elements_to_add = []
        weight_available = max_weight
        for row_id in range(len(m) - 1, 0, -1):
            if k[row_id][weight_available] == 1:
                elements_to_add.append(row_id - 1)
                weight_available = weight_available - weights[row_id - 1]
        elements_to_add.reverse()
        return elements_to_add

class Knapsack_0_1Test(unittest.TestCase):

    def setUp(self):
        self.knapsack = Knapsack_0_1()

    def test_with_small_data_set(self):
        max_weight = 26
        weights = [12, 7, 11, 8, 9]
        values = [24, 13, 23, 15, 16]
        expected_objects_in_the_knapsack = [1, 2, 3]
        actual_objects_in_the_knapsack = self.knapsack.solve(max_weight,
                                                             weights,
                                                             values)
        self.assertEqual(expected_objects_in_the_knapsack,
                         actual_objects_in_the_knapsack)

    def test_with_large_data_set(self):
        max_weight = 6404180
        weights = [382745, 799601, 909247, 729069, 467902, 44328,
                   34610, 698150, 823460, 903959, 853665, 551830,
                   610856, 670702, 488960, 951111, 323046, 446298,
                   931161, 31385, 496951, 264724, 224916, 169684]
        values = [825594, 1677009, 1676628, 1523970, 943972, 97426,
                  69666, 1296457, 1679693, 1902996, 1844992, 1049289,
                  1252836, 1319836, 953277, 2067538, 675367, 853655,
                  1826027, 65731, 901489, 577243, 466257, 369261]
        expected_objects_in_the_knapsack = [0, 1, 3, 4, 5, 9, 10, 
                                            12, 15, 21, 22, 23]
        actual_objects_in_the_knapsack = self.knapsack.solve(max_weight,
                                                             weights,
                                                             values)
        self.assertEqual(expected_objects_in_the_knapsack,
                         actual_objects_in_the_knapsack)

if __name__ == "__main__":
    unittest.main()
