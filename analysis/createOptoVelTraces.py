import os
import pandas as pd
import numpy as np

data_dir = r'C:/Users/angie/Box/EyeSeeCam/data/eyeLink_session/'
os.chdir(data_dir)

# Load opto track data
optoDF = pd.read_csv('optoTidyDF.csv')

subjects = optoDF.subject.unique()
conditions = optoDF.condition.unique()
delays = optoDF.delay.unique()
trials = optoDF.trial.unique()
markers = optoDF.marker.unique()
directions = optoDF.direction.unique()

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
    timeVals = []
    velocityVals = []

    for sub in subjects:
        for cond in conditions:
            for d in delays:
                for t in trials:
                    for mar in markers:

                        data = optoDF.loc[(optoDF.subject == sub) & (optoDF.condition == cond) & (optoDF.delay == d) & (optoDF.trial == t) & (optoDF.marker == mar)]

                        if len(data) == 0:
                            print('Subject: ' + sub + ' condition: ' + cond + ' delay: ' + str(d) + ' trial: ' + str(t) + ' marker: ' + str(mar) + ' does not exist')
                            if len(data) == 8750:
                                print('Trial is complete. 35 seconds')
                            else:
                                print('Length of data is ' + str(len(data)))
                        else:
                            print('working on subject: ' + sub + ' condition: ' + cond + ' delay: ' + str(d) + ' trial: ' + str(t) + ' marker: ' + str(mar))

                            now_x_position, previous_x_position = getNowandPrevious(data.position[data.direction == 'x'])
                            now_y_position, previous_y_position = getNowandPrevious(data.position[data.direction == 'y'])
                            now_z_position, previous_z_position = getNowandPrevious(data.position[data.direction == 'z'])

                            now_time, previous_time = getNowandPrevious(data.time[data.direction == 'x'])
                            real_now_time = now_time - now_time[0]
                            real_previous_time = previous_time - now_time[0]

                            # Calculate 3D position
                            marker3d_position = np.sqrt((now_x_position - previous_x_position) **2
                                                        + (now_y_position - previous_y_position) **2
                                                        + (now_z_position - previous_z_position) **2)

                            timeDifference = real_now_time - real_previous_time

                            velocity = marker3d_position/timeDifference

                            subL = [sub] * len(velocity)
                            condL = [cond] * len(velocity)
                            delayL = [d] * len(velocity)
                            trialL = [t] * len(velocity)
                            marL = [mar] * len(velocity)
                            timeL = real_now_time

                        subVals.append(subL)
                        condVals.append(condL)
                        delayVals.append(delayL)
                        trialVals.append(trialL)
                        marVals.append(marL)
                        timeVals.append(timeL)
                        velocityVals.append(velocity)

    return subVals, condVals, delayVals, trialVals, marVals, timeVals, velocityVals
subVals, condVals, delayVals, trialVals, marVals, timeVals, velocityVals = makeVelDF()

list_of_lists = [subVals, condVals, delayVals, trialVals, marVals, timeVals, velocityVals]
flatL = makeFlatList(list_of_lists)

frames = {'subject': flatL[0], 'condition': flatL[1], 'delay':flatL[2], 'trial':flatL[3], 'marker': flatL[4], 'time': flatL[5], 'velocity': flatL[6]}
df = pd.DataFrame(frames)

df.to_csv(data_dir + 'optoVelocity.csv', index=False)
