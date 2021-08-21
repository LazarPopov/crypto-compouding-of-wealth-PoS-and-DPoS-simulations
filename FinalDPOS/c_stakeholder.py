import uuid

class Stakeholder:
    def __init__(self, id: int, initial_stake_distribution: float):
        self.id = id
        self.stake_distribution = initial_stake_distribution

        self.initial_stake_distribution = self.stake_distribution
        self.initial_fractional_stake = 0
        self.fractional_stake = 0

    def set_initial_fractional_stake(self, total_stake):
        self.initial_fractional_stake = sum(self.initial_stake_distribution) / total_stake
        self.fractional_stake = self.initial_fractional_stake

    def update_fractional_stake(self, total_stake):
        self.fractional_stake = sum(self.stake_distribution) / total_stake


    def vote_proportion(self,stakeholders, delegate):
        votes_for_delegate = 0
        for st in stakeholders:
            votes_for_delegate = st.stake_distribution[delegate] + votes_for_delegate
            #print(f'st.stake_distribution {st.stake_distribution}')
        proportion = self.stake_distribution[delegate]/votes_for_delegate
        return proportion
