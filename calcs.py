import pandas as pd
import numpy as np

data = pd.read_csv('2021data.csv')
data = data.replace({np.nan: ''})

state_names = ['000_0out', '100_0out', '020_0out', '120_0out', '003_0out', '103_0out', '023_0out', '123_0out',
               '000_1out', '100_1out', '020_1out', '120_1out', '003_1out', '103_1out', '023_1out', '123_1out',
               '000_2out', '100_2out', '020_2out', '120_2out', '003_2out', '103_2out', '023_2out', '123_2out']
batter_event_trans_occurrences = pd.DataFrame(np.zeros(shape=(25,24)), columns=state_names)


def determine_start_state(event_record):
    '''

    :param event_record: one line from retrosheet event file
    :return: start state
    '''
    r1 = 1
    r2 = 1
    r3 = 1
    if row['run_on_1st'] == '':  # not a runner on 1st
        r1 = 0
    if row['run_on_2nd'] == '':  # not a runner on 2nd
        r2 = 0
    if row['run_on_3rd'] == '':  # not a runner on 3rd
        r3 = 0

    return r1 + 2 * r2 + 4 * r3 + 8 * row['outs']

def determine_end_state(event_record):
    '''

    :param event_record:
    :return: end state
    '''

    if row['outs'] + row['outs_made'] == 3: # if inning already over
        return 24
    else:
        r1 = 0
        r2 = 0
        r3 = 0
        dests = [row['bat_dest'], row['run_1st_dest'], row['run_2nd_dest'], row['run_3rd_dest']]
        if 1 in dests:
            r1 = 1
        if 2 in dests:
            r2 = 1
        if 3 in dests:
            r3 = 1

        return r1 + 2 * r2 + 4 * r3 + 8 * (row['outs'] + row['outs_made'])

for index, row in data.iterrows():
    # check if batter event!
    if row['is_batter_event'] == 'F':
        continue
    else:

        start_state = determine_start_state(row)
        end_state = determine_end_state(row)

        # update occurrence matrix
        batter_event_trans_occurrences.iloc[end_state, start_state] = batter_event_trans_occurrences.iloc[end_state, start_state] + 1

print(batter_event_trans_occurrences)
