import pandas as pd
from numpy.random import choice
from numpy.random import binomial
runs_scored_transition_matrix_filepath = "Batter Event Transition Matrix 6_21 - Runs Scored.csv"
runs_scored_nb_transition_matrix_filepath = "Batter Event Transition Matrix 6_21 - Runs Scored NB.csv"

RUNS_SCORED_FROM_TRANSITION_MATRIX = pd.read_csv(runs_scored_transition_matrix_filepath, header=None)
RUNS_SCORED_FROM_NB_TRANSITION_MATRIX = pd.read_csv(runs_scored_nb_transition_matrix_filepath, header=None)
LIST_OF_NEXT_STATES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
PROB_OF_BATTER_EVENT = [0.9997968306, 0.9323279925, 0.962289745, 0.9589141599, 0.9868421053,
                        0.9311440678, 0.9850968703, 0.9829396325, 0.9998761303, 0.9177976558,
                        0.9452313503, 0.9455992923, 0.9857320099, 0.9129989765, 0.9827696235,
                        0.9766885834, 0.9998074924, 0.8964528302, 0.9519259041, 0.9562724014,
                        0.982067913, 0.8667889908, 0.9817302526, 0.975175644]
END_STATE = 24

# Inning contains & updates batter event transition matrices as the inning progresses
# Inning keeps track of the score during the inning, and determines when the inning ends.
# Inning can exist in two states: extra innings and normal inning
# ISSUE (Resolved): Right now, we can't report whether the inning progressed from one state to the next by means of a
# batter event or a non batter event. We can repair this by changing what process_step returns. It could return
# runs scored AND the means by which those runs were scored.


class Inning:
    def __init__(self, starting_batter_transition_matrix, starting_non_batter_transition_matrix,
                 extra_inning_status=False, top_of_inning=True):
        self.top_inning_event_engine = Event(starting_batter_transition_matrix, starting_non_batter_transition_matrix)
        self.bottom_inning_event_engine = Event(starting_batter_transition_matrix, starting_non_batter_transition_matrix)
        self.is_extra_inning = extra_inning_status
        self.is_top_of_inning = top_of_inning
        self.top_inning_path = []
        self.bottom_inning_path = []
        self.home_team_inning_score = 0
        self.away_team_inning_score = 0

    def run_inning(self):
        inning_results = None
        while inning_results is None:
            inning_results = self.process_inning_event()
        return inning_results

    def process_inning_event(self):
        if self.is_top_of_inning:
            event_log = self.top_inning_event_engine.process_step()
            self.away_team_inning_score += event_log["runs_scored"]
            self.top_inning_path.append(event_log)
            if self.top_inning_event_engine.get_state() == END_STATE:
                self.is_top_of_inning = False
        else:
            event_log = self.bottom_inning_event_engine.process_step()
            self.home_team_inning_score += event_log["runs_scored"]
            self.bottom_inning_path.append(event_log)
            if self.bottom_inning_event_engine.get_state() == END_STATE:
                return self.end_inning()
        return None

    def end_inning(self):
        return {"Home Team Score": self.home_team_inning_score,
                "Away Team Score": self.away_team_inning_score,
                "Top of Inning Log": self.top_inning_path,
                "Bottom of Inning Log": self.bottom_inning_path}

    def update_transition_matrix(self, transition_matrix, is_batter):
        """

        :param transition_matrix: New transition matrix to be used to update the desired matrix
        :param is_batter: Indicates if transition matrix provided is a batter or non-batter transition matrix
        :return: None
        """
        if is_batter:
            self.inning_event_engine.update_batter_transition_matrix(transition_matrix)
        else:
            self.inning_event_engine.update_non_batter_transition_matrix(transition_matrix)

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
        self.runs_scored_matrix_nb = RUNS_SCORED_FROM_NB_TRANSITION_MATRIX

    def update_batter_transition_matrix(self, new_non_batter_transition_matrix):
        self.non_batter_transition_matrix = new_non_batter_transition_matrix

    def update_non_batter_transition_matrix(self, new_batter_transition_matrix):
        self.batter_transition_matrix = new_batter_transition_matrix

    def calculate_runs_from_transition(self, next_state):
        """

        :param next_state:
        :return:
        """
        if next_state == 24:
            return self.calculate_runs_from_inning_end()
        return self.runs_scored_matrix.iloc[next_state, self.start_state]

    def calculate_runs_from_transition_nb(self, next_state):
        """

        :param next_state:
        :return:
        """
        if next_state == 24:
            return self.calculate_runs_from_inning_end()
        return self.runs_scored_matrix_nb.iloc[next_state, self.start_state]

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

    def get_state(self):
        return self.start_state

    def process_step(self):
        """

        :return:
        """
        runs = 0.0
        if self.is_batter_event():
            outcome = self.determine_next_state_from_batter_event()
            runs = self.calculate_runs_from_transition(outcome)
            self.start_state = outcome
            return {"state": outcome, "runs_scored": runs, "is_batter_event": True}
        else:
            outcome = self.determine_next_state_from_non_batter_event()
            runs = self.calculate_runs_from_transition_nb(outcome)
            self.start_state = outcome
            return {"state": outcome, "runs_scored": runs, "is_batter_event": False}

