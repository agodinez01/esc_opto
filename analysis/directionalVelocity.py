import os
import pandas as pd
import numpy as np

data_dir = r'C:/Users/angie/Box/EyeSeeCam/data/'
os.chdir(data_dir)

# Load opto track data
optoDF = pd.read_csv('optoTidyDF.csv')

subjects = optoDF.subject.unique()
conditions = optoDF.condition.unique()
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
    marVals = []
    dirVals = []
    timeVals = []
    posVals = []
    velVals = []

    for sub in subjects:
        for cond in conditions:
            for mar in markers:
                for dir in directions:

                    data = optoDF.loc[(optoDF.subject == sub) & (optoDF.condition == cond) & (optoDF.marker == mar) & (optoDF.direction == dir)]

                    if len(data) == 0:
                        print(cond + ' and marker ' + str(mar) + dir + ' does not exist in ' + sub + 's file')
                        continue
                    else:
                        print('working on ' + sub + ' ' + cond + ' ' + str(mar) + dir)

                        nowPosition, previousPosition = getNowandPrevious(data.position)

                        velocity = (nowPosition - previousPosition)/ sampleDifference

                        subL = [sub] * len(velocity)
                        condL = [cond] * len(velocity)
                        marL = [mar] * len(velocity)
                        dirL = [dir] * len(velocity)

                    subVals.append(subL)
                    condVals.append(condL)
                    marVals.append(marL)
                    dirVals.append(dirL)
                    timeVals.append(data.time)
                    posVals.append(data.position)
                    velVals.append(velocity)


    return subVals, condVals, marVals, dirVals, timeVals, posVals, velVals
subL, condL, marL, dirL, timeL, posL, velL = makeDirectionalVelocity()

list_of_lists = [subL, condL, marL, dirL, timeL, posL, velL]
flatL = makeFlatList(list_of_lists)

frames = {'subject': flatL[0], 'condition': flatL[1], 'marker': flatL[2], 'direction': flatL[3], 'time': flatL[4], 'position': flatL[5], 'velocity': flatL[6]}
df = pd.DataFrame(frames)

df.to_csv(data_dir + 'optoPositionVelocity.csv', index=False)