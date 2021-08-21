from typing import List
from numpy import median
import numpy as np
import matplotlib.pyplot as plt
from itertools import accumulate
from bisect import bisect



from c_c_node import Node
from c_c_tester import Tester
import random
import csv
import time


class Simulation:

    def __init__(self, stake_distribution, block_interval,  R, T):
        self.number_of_nodes = 0
        self.nodes = []
        self.blocks = 0
        self.block_interval = block_interval
        self.initial_stakes = []
        self.R = R
        self.T = T

        for stake in stake_distribution:
                validator = Node(self.number_of_nodes, stake)

                self.number_of_nodes += 1
                self.nodes.append(validator)

        total_stake = self.get_total_stake()

        for node in self.nodes:
            node.set_initial_fractional_stake(total_stake)
    def selection_of_proposer(self,nodes):
        weights = []
        for node in nodes:
            weights.append(node.stake)
        prop = random.choices(nodes, weights)
        return prop[0]
    def get_total_stake(self):
        return sum([node.stake for node in self.nodes])
    def stakes(self):
        stakes = []
        stakes.append([node.stake for node in self.nodes])
        return stakes

    def propotional_sampling(self, nodes):
        # calculate cumulative sum from A:
        A = []
        for node in nodes:
            A.append(node.stake/self.get_total_stake())
        # print(A)
        cum_sum = [*accumulate(A)]
        # cum_sum = [0, 5, 32, 38, 51, 79, 179, 224, 234, 313]

        i = random.random()                     # i = [0.0, 1.0)
        idx = bisect(cum_sum, i*cum_sum[-1])    # get index to list A
        # print(idx)
        return idx

    def generate_reward(self, step, R, T):
        #geometric reward
            #reward = (1+R)**(step/T)-(1+R)**((step-1)/T)
        #constant reward
            reward =  R/T
            
        return reward
    def run(self, steps, should_print_intermediate_states, experiment=None):
        # self.print_state(0)
        run_at_time=time.time()

        #calculate equitability for abitrary party:
        arb_stakeholder = random.choice(self.nodes)
        first_term = ((arb_stakeholder.initial_fractional_stake/self.get_total_stake()) - (arb_stakeholder.initial_fractional_stake/self.get_total_stake())**2)
        second_term = 1
        product_second_term = 1
        total_stake_at_0_squared = self.get_total_stake()**2

        for step in range(1, steps + 1):
            # proposer = self.nodes[self.propotional_sampling(self.nodes)]
            proposer = self.selection_of_proposer(self.nodes)
            reward = self.generate_reward(step, self.R, self.T)
            prev=proposer.stake
            proposer.stake += reward

            #calculate equitability for abitrary party:
            #S(n) total stake at n

            if step == 1:
                total_stake_step = self.get_total_stake()
            else:
                total_stake_step_minus_1 = total_stake_step
                total_stake_step = self.get_total_stake()
                product_second_term = total_stake_step/total_stake_step_minus_1*product_second_term
            if step == self.T:
                total_stake_at_T_squared = self.get_total_stake()**2

            if should_print_intermediate_states:
                pass
                self.print_state(step)

            experiment.collect(
                Tester.gini_coefficient(self.nodes),
                Tester.equitability(self.nodes),
                1 + step // self.block_interval,
                reward,
                self.get_total_stake()/self.number_of_nodes,
                median(self.stakes()),
                np.std(self.stakes())
            )
            with open('all_values_per_tick_constant.csv', mode='a') as value_file:
                value_writer = csv.writer(value_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator = '\n')
                value_writer.writerow([run_at_time, step, Tester.gini_coefficient(self.nodes), Tester.equitability(self.nodes), reward, self.get_total_stake()/self.number_of_nodes, median(self.stakes()),np.std(self.stakes())])

            total_stake = self.get_total_stake()

            [node.update_fractional_stake(total_stake) for node in self.nodes]
        # x = []
        # y = []
        # print(self.get_total_stake())
        # for node in self.nodes:
        #     x.append(node.stake/self.get_total_stake())
        #     y.append(node.stake)
        # print(y)
        # plt.hist(x, density=True, bins=50)
        # plt.title("Constant fractional stakes")
        # plt.show()
        # plt.hist(y, density=True, bins=50)
        # plt.title("Constant stakes")
        # plt.show()

        #calculate equitability for abitrary party:
        second_term = 1 - total_stake_at_0_squared/total_stake_at_T_squared*product_second_term
        var = first_term*second_term
        # print(f'total_stake_at_0_squared  {total_stake_at_0_squared}')
        # print(f'total_stake_at_T_squared  {total_stake_at_T_squared}')
        # print(f'product_second_term  {product_second_term}')
        var = first_term*second_term
        # print(f'var  {var}')

        if not should_print_intermediate_states:
            self.print_state(steps)
            pass

    def print_state(self, step):
        print()
        print("POS_CONSTANT")
        print(f'Step #{step}:')
        print()

        print(f'Total stake {self.get_total_stake()}')
        print(f'Equitability = {Tester.equitability(self.nodes)}')
        print(f"Gini coefficient = {Tester.gini_coefficient(self.nodes)}")
        print()

        # for node in self.nodes:
        #     print(f"Node `{node.id}` has stake = {node.stake}")

        print()
        print('----------------')
