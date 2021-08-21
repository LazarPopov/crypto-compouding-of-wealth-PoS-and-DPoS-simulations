from c_c_simulation import Simulation
from c_c_experiment import Experiment
from numpy import random

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

    steps = block_interval * epochs
    nodes = []

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

                        stakes.append(float(st)/10000 )
                    delegate_number=delegate_number+1

                if not sum(stakes) ==0:
                    nodes.append(sum(stakes))
    elif data == 1:
        print ("DATA: uniform")
        for i in range(number_of_nodes):
            nodes.append(starting_stake_per_node)


    def handler(experiment):
        sim = Simulation(nodes, block_interval, R, T )
        sim.run(steps=steps, should_print_intermediate_states= False, experiment=experiment)

    experiment = Experiment(block_interval, epochs, run_handler=handler)
    experiment.run(10)
    # experiment.save()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
