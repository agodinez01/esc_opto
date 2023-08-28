import os
import pandas as pd
import numpy as np

data_dir = r'C:/Users/angie/Box/EyeSeeCam/data/eyeLink_session/'
os.chdir(data_dir)

# Load opto track data
eyeLinkDF = pd.read_csv('elTidyDF.csv')

subjects = eyeLinkDF.subject.unique()
conditions = eyeLinkDF.condition.unique()
delays = eyeLinkDF.delay.unique()
trials = eyeLinkDF.trial.unique()
markers = eyeLinkDF.marker.unique()
directions = eyeLinkDF.direction.unique()

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
                        for dir in directions:

                            data = eyeLinkDF.loc[(eyeLinkDF.subject == sub) & (eyeLinkDF.condition == cond) & (eyeLinkDF.delay == d) & (eyeLinkDF.trial == t) & (eyeLinkDF.marker == mar) & (eyeLinkDF.direction == dir)]

                            if len(data) == 0:
                                print('Subject: ' + sub + ' condition: ' + cond + ' delay: ' + str(d) + ' trial: ' + str(t) + ' does not exist')
                                continue
                            else:
                                print('working on subject: ' + sub + ' condition: ' + cond + ' delay: ' + str(d) + ' trial: ' + str(t))

                                nowPosition, previousPosition = getNowandPrevious(data.position)
                                nowTime, previousTime = getNowandPrevious(data.retrieveTime)

                                velocity_sampleTime = (nowPosition - previousPosition)/ sampleDifference
                                velocity_retrieveTime = (nowPosition - previousPosition)/ (nowTime - previousTime)

                                subL = [sub] * len(velocity_sampleTime)
                                condL = [cond] * len(velocity_sampleTime)
                                delayL = [d] * len(velocity_sampleTime)
                                trialL = [t] * len(velocity_sampleTime)
                                marL = [mar] * len(velocity_sampleTime)
                                dirL = [dir] * len(velocity_sampleTime)

                                subVals.append(subL)
                                condVals.append(condL)
                                delayVals.append(delayL)
                                trialVals.append(trialL)
                                marVals.append(marL)
                                dirVals.append(dirL)
                                sampleTimeVals.append(data.frameTime)
                                retrieveTimeVals.append(data.retrieveTime)
                                posVals.append(data.position)
                                sampleVelVals.append(velocity_sampleTime)
                                retrieveVelVals.append(velocity_retrieveTime)

    return subVals, condVals, delayVals, trialVals, marVals, dirVals, sampleTimeVals, retrieveTimeVals, posVals, sampleVelVals, retrieveVelVals
subL, condL, delayL, trialL, marL, dirL, sampleTimeL, retrieveTimeL, posL, sampleVelL, retrieveVelL = makeDirectionalVelocity()

list_of_lists = [subL, condL, delayL, trialL, marL, dirL, sampleTimeL, retrieveTimeL, posL, sampleVelL, retrieveVelL]
flatL = makeFlatList(list_of_lists)

frames = {'subject':flatL[0], 'condition':flatL[1], 'delay':flatL[2], 'trial':flatL[3], 'marker':flatL[4], 'direction':flatL[5], 'sampleTime':flatL[6], 'retrieveTime':flatL[7], 'position':flatL[8], 'sampleVelocity':flatL[9], 'retrieveVelocity':flatL[10]}
df = pd.DataFrame(frames)

df.to_csv(data_dir + 'elPositionVelocity.csv', index=False)