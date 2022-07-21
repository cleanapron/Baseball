import pandas as pd
from numpy.random import choice
from states import Event, Inning

# draw = choice(list_of_candidates, number_of_items_to_pick,
#               p=probability_distribution)

LIST_OF_NEXT_STATES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                      19, 20, 21, 22, 23, 24]


def get_batter_transition_matrix():
    """
    
    :return: Batter Transition Matrix
    """
    transition_matrix_filepath = "~/Downloads/Batter Event Transition Matrix 6_21 - Sheet1.csv"
    return pd.read_csv(transition_matrix_filepath, header=None)


def get_non_batter_transition_matrix():
    """
    Helper function to get non batter transition matrix for assistance in testing
    :return: Non Batter Transition Matrix
    """
    transition_matrix_filepath = "~/Downloads/Batter Event Transition Matrix 6_21 - Non Batter Event Probability Matrix.csv"
    return pd.read_csv(transition_matrix_filepath, header=None)


def batter_event(start_state):
    """
    
    :param start_state: 
    :return: 
    """
    tm = get_batter_transition_matrix()
    next_state = choice(LIST_OF_NEXT_STATES, 1, p=tm[start_state])
    return next_state


def test():
    results = []

    for i in range(1000):
        results.append(batter_event(0)[0])

    print(results.count(0) / 1000, "should be ~ 0.035")
    print(results.count(1) / 1000, "should be ~ 0.239")
    print(results.count(2) / 1000, "should be ~ 0.048")
    print(results.count(4) / 1000, "should be ~ 0.002")
    print(results.count(8) / 1000, "should be ~ 0.676")



def test_determine_next_state_from_batter_event():
    results = []
    test_event = Event(get_batter_transition_matrix(), get_non_batter_transition_matrix())

    for i in range(1000):
        results.append(test_event.determine_next_state_from_batter_event()[0])

    print(results.count(0) / 1000, "should be ~ 0.035")
    print(results.count(1) / 1000, "should be ~ 0.239")
    print(results.count(2) / 1000, "should be ~ 0.048")
    print(results.count(4) / 1000, "should be ~ 0.002")
    print(results.count(8) / 1000, "should be ~ 0.676")


def test_calculate_runs_from_transition():
    test_event = Event(get_batter_transition_matrix(), get_non_batter_transition_matrix())
    print(test_event.calculate_runs_from_transition(0, 0), "should be 1")
    print(test_event.calculate_runs_from_transition(0, 1), "should be 2")
    print(test_event.calculate_runs_from_transition(0, 2), "should be 2")
    print(test_event.calculate_runs_from_transition(0, 3), "should be 3")
    print(test_event.calculate_runs_from_transition(0, 4), "should be 2")
    print(test_event.calculate_runs_from_transition(0, 5), "should be 3")


def test_batter_or_non_batter_event():
    test_event = Event(get_batter_transition_matrix(), get_non_batter_transition_matrix())
    counter = 0
    for i in range(10000):
        if test_event.is_batter_event():
            counter += 1
    print(counter/10000)


#test()
# test_determine_next_state_from_batter_event()
# test_calculate_runs_from_transition()
# test_batter_or_non_batter_event()

def test_process_step():
    test_event = Event(get_batter_transition_matrix(), get_non_batter_transition_matrix())
    runs_total = 0.0
    for i in range(10):
        print(test_event.process_step(), "runs were scored")
        if test_event.start_state == 24:
            print("inning is over")
            break


def test_inning_class():
    test_inning = Inning(get_batter_transition_matrix(), get_non_batter_transition_matrix())
    print(test_inning.run_inning())
          # , '\n',  'top inning path', test_inning.top_inning_path,
          # '\n', 'bottom inning path', test_inning.bottom_inning_path)


# for i in range(9):
#     test_inning_class()
#test_process_step()

test_inning_class()