import os
import pandas as pd
import numpy as np

eye_tracking = 1 # EyeSeeCam = 0; EyeLink = 1

if eye_tracking == 0:
    data_dir = r'C:/Users/angie/Box/EyeSeeCam/data/esc_session/'
elif eye_tracking == 1:
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

sampleDifference = 0.004 # Sample at 250 Hz

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

def makeDirectionalVelocity():
    subVals = []
    condVals = []
    delayVals = []
    trialVals = []
    marVals = []
    dirVals = []
    timeVals = []
    posVals = []
    velVals = []

    for sub in subjects:
        for cond in conditions:
            for d in delays:
                for t in trials:
                    for mar in markers:
                        for dir in directions:

                            data = optoDF.loc[(optoDF.subject == sub) & (optoDF.condition == cond) & (optoDF.delay == d) & (optoDF.trial == t) & (optoDF.marker == mar) & (optoDF.direction == dir)]

                            if len(data) == 0:
                                print('Subject: ' + sub + ' condition: ' + cond + ' delay: ' + str(d) + ' trial: ' + str(t) + ' does not exist')
                                continue
                            else:
                                print('working on subject: ' + sub + ', Condition: ' + cond + ', Delay: ' + str(d) + ' and Trial: ' + str(t))

                                nowPosition, previousPosition = getNowandPrevious(data.position)

                                velocity = (nowPosition - previousPosition)/ sampleDifference

                                subL = [sub] * len(velocity)
                                condL = [cond] * len(velocity)
                                delayL = [d] * len(velocity)
                                trialL = [t] * len(velocity)
                                marL = [mar] * len(velocity)
                                dirL = [dir] * len(velocity)

                            subVals.append(subL)
                            condVals.append(condL)
                            delayVals.append(delayL)
                            trialVals.append(trialL)
                            marVals.append(marL)
                            dirVals.append(dirL)
                            timeVals.append(data.time)
                            posVals.append(data.position)
                            velVals.append(velocity)


    return subVals, condVals, delayVals, trialVals, marVals, dirVals, timeVals, posVals, velVals
subL, condL, delayL, trialL, marL, dirL, timeL, posL, velL = makeDirectionalVelocity()

list_of_lists = [subL, condL, delayL, trialL, marL, dirL, timeL, posL, velL]
flatL = makeFlatList(list_of_lists)

frames = {'subject': flatL[0], 'condition': flatL[1], 'delay':flatL[2], 'trial':flatL[3], 'marker': flatL[4], 'direction': flatL[5], 'time': flatL[6], 'position': flatL[7], 'velocity': flatL[8]}
df = pd.DataFrame(frames)

df.to_csv(data_dir + 'optoPositionVelocity.csv', index=False)