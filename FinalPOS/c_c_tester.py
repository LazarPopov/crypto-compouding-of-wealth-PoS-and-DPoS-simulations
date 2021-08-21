from c_c_node import Node
import c_c_simulation

class Tester:

    @staticmethod
    def gini_coefficient(nodes):
        numerator_sum = 0
        for i in range(len(nodes)):
            stake_i = nodes[i].stake
            # print(stake_i)
            for j in range(len(nodes)):
                stake_j = nodes[j].stake
                numerator_sum += abs(stake_i - stake_j)

        average = sum(node.stake for node in nodes) / len(nodes)
        # print(f'Step #{step}:')
        return numerator_sum / (2 * (len(nodes) ** 2) * average)

    @staticmethod
    def equitability(nodes):
        # For now, only call this at the end of the simulation.
        # Has to be adjusted to work for intermediate steps.
        epsilon_vector = []
        for node in nodes:
            average = sum(node.fractional_stake for node in nodes) / len(nodes)
            sum_variance = 0
            for n in nodes:
                sum_variance += (n.fractional_stake - average) ** 2
            variance = sum_variance / (len(nodes) - 1)
            epsilon = variance / (node.initial_fractional_stake * (1 - node.initial_fractional_stake))
            epsilon_vector.append(epsilon)

        return min(epsilon_vector)
