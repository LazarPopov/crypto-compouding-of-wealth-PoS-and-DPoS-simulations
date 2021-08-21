from c_stakeholder import Stakeholder
import c_simulation

class Tester:

    @staticmethod
    def gini_coefficient(stakeholders):
        numerator_sum = 0
        for i in range(len(stakeholders)):
            stake_i = sum(stakeholders[i].stake_distribution)

            for j in range(len(stakeholders)):
                stake_j = sum(stakeholders[j].stake_distribution)
                numerator_sum += abs(stake_i - stake_j)

        sumStakes=0
        for stakeholder in stakeholders:
            sumStakes=sumStakes+sum(stakeholder.stake_distribution)
        average = sumStakes / len(stakeholders)

        return numerator_sum / (2 * (len(stakeholders) ** 2) * average)

    @staticmethod
    def equitability(stakeholders):
        # For now, only call this at the end of the simulation.
        # Has to be adjusted to work for intermediate steps.
        epsilon_vector = []
        for stakeholder in stakeholders:
            average = sum(stakeholder.fractional_stake for stakeholder in stakeholders) / len(stakeholders)
            sum_variance = 0
            for sth in stakeholders:
                sum_variance += (sth.fractional_stake - average) ** 2
            variance = sum_variance / (len(stakeholders) - 1)
            epsilon = variance / (stakeholder.initial_fractional_stake * (1 - stakeholder.initial_fractional_stake))
            epsilon_vector.append(epsilon)
        # print(f'epsilon_vector size: {len(epsilon_vector)}' )
        # print(epsilon_vector)
        return min(epsilon_vector)
