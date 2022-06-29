import pandas as pd
from numpy.random import choice
from numpy.random import binomial
runs_scored_transition_matrix_filepath = "~/Downloads/Batter Event Transition Matrix 6_21 - Runs Scored.csv"

RUNS_SCORED_FROM_TRANSITION_MATRIX = pd.read_csv(runs_scored_transition_matrix_filepath, header=None)
LIST_OF_NEXT_STATES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
PROB_OF_BATTER_EVENT = [0.9997968306, 0.9323279925, 0.962289745, 0.9589141599, 0.9868421053,
                        0.9311440678, 0.9850968703, 0.9829396325, 0.9998761303, 0.9177976558,
                        0.9452313503, 0.9455992923, 0.9857320099, 0.9129989765, 0.9827696235,
                        0.9766885834, 0.9998074924, 0.8964528302, 0.9519259041, 0.9562724014,
                        0.982067913, 0.8667889908, 0.9817302526, 0.975175644]

# class Inning:
#     current_state = 0
#
#     def __init__(self):

# Goals for this class:
# We should give it transition matrices (can change)
# We should give it a batter event probability vector
# We should give it a start position
# We should expect it to return an ending position
# Inning should calculate changes in score from one state to the next


class Event:
    def __init__(self, current_batter_transition_matrix, current_non_batter_transition_matrix):
        self.start_state = 0
        self.batter_transition_matrix = current_batter_transition_matrix
        self.non_batter_transition_matrix = current_non_batter_transition_matrix
        self.runs_scored_matrix = RUNS_SCORED_FROM_TRANSITION_MATRIX

    def calculate_runs_from_transition(self, next_state):
        """

        :param next_state:
        :return:
        """
        if next_state == 24:
            return self.calculate_runs_from_inning_end()
        return self.runs_scored_matrix.iloc[next_state, self.start_state]

    def calculate_runs_from_inning_end(self):
        # TODO Calculate using probabilities from excel
        """

        :return:
        """
        return 0

    def determine_next_state_from_batter_event(self):
        """
        Uses the transition matrix to calculate a next state
        :param start_state:
        :return:
        """
        return choice(LIST_OF_NEXT_STATES, 1, p=self.batter_transition_matrix[self.start_state])[0]

    def determine_next_state_from_non_batter_event(self):
        """
        Uses the transition matrix to calculate a next state
        :param start_state:
        :return:
        """
        return choice(LIST_OF_NEXT_STATES,1,p=self.non_batter_transition_matrix[self.start_state])[0]


    def is_batter_event(self):
        """

        :return:
        """
        batter_event_probability = PROB_OF_BATTER_EVENT[self.start_state]
        return binomial(1, batter_event_probability) == 1

    def process_step(self):
        """

        :return:
        """
        runs = 0.0
        if self.is_batter_event():
            outcome = self.determine_next_state_from_batter_event()
            print("outcome", outcome)
            runs = self.calculate_runs_from_transition(outcome)
            self.start_state = outcome
        else:
            print("NONBATTER EVENT!!!!!")
            outcome = self.determine_next_state_from_non_batter_event()
            print("outcome", outcome)
            runs = self.calculate_runs_from_transition(outcome)
            self.start_state = outcome
        return runs














