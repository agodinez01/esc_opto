import os
import pandas as pd
import numpy as np

data_dir = r'C:/Users/angie/Box/EyeSeeCam/data/eyeLink_session/'
os.chdir(data_dir)

# Load EL data
eyeLinkDF = pd.read_csv('elTidyDF.csv')

subjects = eyeLinkDF.subject.unique()
conditions = eyeLinkDF.condition.unique()
delays = eyeLinkDF.delay.unique()
trials = eyeLinkDF.trial.unique()
markers = eyeLinkDF.marker.unique()
directions = eyeLinkDF.direction.unique()

# Function to make flat list
def makeFlatList(input_list):
    flatL = []

    for idx, itemL in enumerate(input_list):
        flat_list = [item for sublist in input_list[idx] for item in sublist]
        flatL.append(flat_list)

    return flatL

# Function for sensor now and sensor previous
def getNowandPrevious(data):

    # Convert to numpy array in order to be able to subtract later
    now_position = data.to_numpy()
    previous_position = pd.Series(np.hstack((data[-1:], data[:-1]))).to_numpy()

    return now_position, previous_position

def makeVelDF():
    subVals = []
    condVals = []
    delayVals = []
    trialVals = []
    marVals = []
    sampleTimeVals = []
    retrieveTimeVals = []
    posVals = []
    sampleVelVals = []
    retrieveVelVals = []

    for sub in subjects:
        for cond in conditions:
            for d in delays:
                for t in trials:
                    for mar in markers:

                        data = eyeLinkDF.loc[(eyeLinkDF.subject == sub) & (eyeLinkDF.condition == cond) & (eyeLinkDF.delay == d) & (eyeLinkDF.trial == t) & (eyeLinkDF.marker == mar)]

                        if len(data) == 0:
                            print('Subject: ' + sub + ' condition: ' + cond + ' delay: ' + str(d) + ' trial: ' + str(t) + ' marker: ' + str(mar) + ' does not exist')
                            continue
                        else:
                            print('working on subject: ' + sub + ' condition: ' + cond + ' delay: ' + str(d) + ' trial: ' + str(t) + ' marker: ' + str(mar))

                        now_x_position, previous_x_position = getNowandPrevious(data.position[data.direction == 'x'])
                        now_y_position, previous_y_position = getNowandPrevious(data.position[data.direction == 'y'])

                        sample_now_time, sample_previous_time = getNowandPrevious(data.frameTime[data.direction == 'x'])
                        sample_real_now_time = sample_now_time - sample_now_time[0]
                        sample_real_previous_time = sample_previous_time - sample_now_time[0]

                        retrieved_now_time, retrieved_previous_time = getNowandPrevious(data.retrieveTime[data.direction == 'x'])
                        retrieved_real_now_time = retrieved_now_time - retrieved_now_time[0]
                        retrieved_real_previous_time = retrieved_previous_time - retrieved_now_time[0]

                        # Calculate 2D position
                        marker2D_position = np.sqrt((now_x_position - previous_x_position) **2
                                                    + (now_y_position - previous_y_position) **2)

                        sample_time_difference = sample_real_now_time - sample_real_previous_time
                        retrieved_time_difference = retrieved_real_now_time - retrieved_real_previous_time

                        sample_velocity = marker2D_position/ sample_time_difference
                        retrieved_velocity = marker2D_position/ retrieved_time_difference

                        subL = [sub] * len(sample_velocity)
                        condL = [cond] * len(sample_velocity)
                        delayL = [d] * len(sample_velocity)
                        trialL = [t] * len(sample_velocity)
                        marL = [mar] * len(sample_velocity)
                        sampleTimeL = sample_real_now_time
                        retreiveTimeL = retrieved_now_time

                        subVals.append(subL)
                        condVals.append(condL)
                        delayVals.append(delayL)
                        trialVals.append(trialL)
                        marVals.append(marL)
                        sampleTimeVals.append(sampleTimeL)
                        retrieveTimeVals.append(retreiveTimeL)
                        sampleVelVals.append(sample_velocity)
                        retrieveVelVals.append(retrieved_velocity)

    return subVals, condVals, delayVals, trialVals, marVals, sampleTimeVals, retrieveTimeVals, sampleVelVals, retrieveVelVals
subVals, condVals, delayVals, trialVals, marVals, sampleTimeVals, retrieveTimeVals, sampleVelVals, retrieveVelVals = makeVelDF()

list_of_lists = [subVals, condVals, delayVals, trialVals, marVals, sampleTimeVals, retrieveTimeVals, sampleVelVals, retrieveVelVals]

flatL = makeFlatList(list_of_lists)

frames = {'subject':flatL[0], 'condition':flatL[1], 'delay':flatL[2], 'trial':flatL[3], 'marker':flatL[4], 'sampleTime':flatL[5], 'retrieveTime':flatL[6], 'sampleVelocity':flatL[7], 'retrieveVelocity':flatL[8]}
df = pd.DataFrame(frames)

df.to_csv(data_dir + 'elVelocity.csv', index=False)
