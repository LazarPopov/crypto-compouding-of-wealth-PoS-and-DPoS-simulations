from c_simulation import Simulation
from c_experiment import Experiment
from numpy import random
from copy import copy, deepcopy


# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    # PARAMETERS
    epochs = 20
    block_interval = 210
    starting_stake_per_node = 10
    number_of_nodes = 100
    T = epochs*block_interval #timesteps
    R = 1000000
    # starting_stake_per_node*number_of_nodes*1 #maximum amount of reward
    number_of_delegates = 7
    data = 1 # 0 = EOS, 1 = random uniform
    runs = 10
    rng = random.RandomState(42)
    random.seed(42)



    stakeholders_stakes=[]
    if data == 0:
        print ("DATA: EOS")
        with open('stakes.txt') as f:
            for line in f:

                stakes = []

                delegate_number=0
                for st in line.split(' '):
                    if delegate_number==number_of_delegates:
                        break
                    if st != ' ' and st != '\n':

                        stakes.append(float(st)/10000   )
                    delegate_number=delegate_number+1

                if not sum(stakes) == 0:
                    stakeholders_stakes.append(stakes)
    elif data == 1:
        print ("DATA: uniform")
        for i in range(100):
            stakeholders_stakes.append([10/number_of_delegates] * number_of_delegates)


    steps = block_interval * epochs


    def handler(experiment):
        #deepcopy needed because coppying 2D array
        stakes_input = deepcopy(stakeholders_stakes)
        sim = Simulation(stakes_input, block_interval, number_of_delegates, R, T)
        sim.run(steps=steps, should_print_intermediate_states=False, experiment=experiment)

    experiment = Experiment(block_interval, epochs, run_handler=handler)
    experiment.run(runs)
    # experiment.save()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
