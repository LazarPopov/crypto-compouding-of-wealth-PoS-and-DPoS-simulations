from typing import List
from numpy import median
import numpy as np
import matplotlib.pyplot as plt
from itertools import accumulate
from bisect import bisect


from c_stakeholder import Stakeholder
from c_tester import Tester
import random
import csv
import time


class Simulation:

    def __init__(self, stakeholders_stakes, block_interval, number_of_delegates, R, T):
        self.number_of_stakeholders = 0
        self.stakeholders = []
        self.number_of_delegates = number_of_delegates
        self.last_chosen_delegate = -1
        self.blocks = 0
        self.block_interval = block_interval
        self.initial_stakes = []
        self. R = R
        self. T = T

        for stakeholders_stake in stakeholders_stakes:
            stakeholder = Stakeholder(self.number_of_stakeholders, stakeholders_stake)

            self.number_of_stakeholders += 1
            self.stakeholders.append(stakeholder)


        total_stake = self.get_total_stake()

        for stakeholder in self.stakeholders:
            stakeholder.set_initial_fractional_stake(total_stake)

    def get_total_stake(self):
        sumStakes = 0
        for stakeholder in self.stakeholders:

            sumStakes=sum(stakeholder.stake_distribution)+sumStakes
        return sumStakes

    def stakes(self):
        stakes = []
        stakes.append([stakeholder.stake_distribution for stakeholder in self.stakeholders])
        return stakes

    #selects delegate where each deleagte has a predetermined slot
    def select_delegate(self):
        if (self.last_chosen_delegate == self.number_of_delegates-1):
            self.last_chosen_delegate = 0
        else: self.last_chosen_delegate=self.last_chosen_delegate+1
        return self.last_chosen_delegate


    def generate_reward(self, step, R, T):
        return R/T

    def run(self, steps, should_print_intermediate_states, experiment=None):
        # self.print_state(0)
        run_at_time=time.time()

        #value_writer.writerow(['run_at_time','step','GINI','EQUITABILITY', 'REWARD' 'average_stakes', 'median_stakes',  'sd_stakes'])
        for step in range(1, steps + 1):
            reward = self.generate_reward(step, self.R, self.T)
            delegate = self.select_delegate()
            random.shuffle(self.stakeholders)
            for stakeholder in self.stakeholders:
                # print(stakeholder.vote_proportion(self.stakeholders, delegate))
                added_reward = stakeholder.vote_proportion(self.stakeholders, delegate)*reward

                # print(f'Added reward {added_reward} from delegate {self.last_chosen_delegate + 1}')
                stakeholder.stake_distribution[delegate] += added_reward

            if should_print_intermediate_states:

                self.print_state(step)

            experiment.collect(
                Tester.gini_coefficient(self.stakeholders),
                Tester.equitability(self.stakeholders),
                1 + step // self.block_interval,
                reward,
                self.get_total_stake()/self.number_of_stakeholders,
                median(self.stakes()),
                np.std(self.stakes())
            )
            with open('all_values_per_tick_dpos.csv', mode='a') as value_file:
                value_writer = csv.writer(value_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,lineterminator = '\n')
                value_writer.writerow([run_at_time, step, Tester.gini_coefficient(self.stakeholders), Tester.equitability(self.stakeholders), reward, self.get_total_stake()/self.number_of_stakeholders, median(self.stakes()),np.std(self.stakes())])

            total_stake = self.get_total_stake()
            [stakeholder.update_fractional_stake(total_stake) for stakeholder in self.stakeholders]

        # x = []
        # y = []
        # for stakeholder in self.stakeholders:
        #     x.append(sum(stakeholder.stake_distribution)/self.get_total_stake())
        # for stakeholder in self.stakeholders:
        #     y.append(sum(stakeholder.stake_distribution))
        #
        # plt.hist(x, density=True, bins=30)
        # plt.title("DPOS fractional stakes")
        # plt.show()
        # plt.hist(y, density=True, bins=50)
        # plt.title("DPOS stakes")
        # plt.show()



        if not should_print_intermediate_states:
            self.print_state(steps)
            pass

    def print_state(self, step):
        print()
        print ("DPOS")
        print(f'Step #{step}:')
        print()

        print(f'Total stake {self.get_total_stake()}')
        print(f'Equitability = {Tester.equitability(self.stakeholders)}')
        print(f"Gini coefficient = {Tester.gini_coefficient(self.stakeholders)}")
        print()

        # for stakeholder in self.stakeholders:
        #     print(f"Stakeholder `{stakeholder.id}` has stake distribution = {stakeholder.stake_distribution}")

        print()
        print('----------------')
