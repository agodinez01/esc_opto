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
    marVals = []
    timeVals = []
    velocityVals = []

    for sub in subjects:
        for cond in conditions:
            for mar in markers:

                data = optoDF.loc[(optoDF.subject == sub) & (optoDF.condition == cond) & (optoDF.marker == mar)]

                if len(data) == 0:
                    print(cond + ' and marker ' + str(mar) + ' does not exist in ' + sub + 's file')
                    continue
                else:
                    print('working on ' + sub + ' ' + cond + ' ' + str(mar))

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
                    marL = [mar] * len(velocity)
                    timeL = real_now_time

                subVals.append(subL)
                condVals.append(condL)
                marVals.append(marL)
                timeVals.append(timeL)
                velocityVals.append(velocity)

    return subVals, condVals, marVals, timeVals, velocityVals
subVals, condVals, marVals, timeVals, velocityVals = makeVelDF()

list_of_lists = [subVals, condVals, marVals, timeVals, velocityVals]
flatL = makeFlatList(list_of_lists)

frames = {'subject': flatL[0], 'condition': flatL[1], 'marker': flatL[2], 'time': flatL[3], 'velocity': flatL[4]}
df = pd.DataFrame(frames)

df.to_csv(data_dir + 'optoVelocity.csv', index=False)
