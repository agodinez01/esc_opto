import os
import pandas as pd
import numpy as np

# Create tidy version of the opto track data

data_dir = r'C:/Users/angie/Box/EyeSeeCam/data/' # It's too large to send via Git. Make sure you download raw_data from the HU Box (ESC/recording_session_20220324)
#save_dir = r'C:/Users/angie/Box/EyeSeeCam/data/'

# Change directory and load optotrak and eyeSeeCam data
os.chdir(data_dir)

escData = pd.read_csv('esc_data.csv')
optoData = pd.read_csv('opto3_data.csv')

subjects = escData.subject.unique()
conditions = escData.condition.unique()
numMarkers = 7
numDirections = 3
samplingRate = 250

# Function to make flat list
def makeFlatList(input_list):
    flatL = []

    for idx, itemL in enumerate(input_list):
        flat_list = [item for sublist in input_list[idx] for item in sublist]
        flatL.append(flat_list)

    return flatL

# Make tidy pandas data frame for opto data
def makeOptoDF():
    subVals = []
    condVals = []
    timeVals = []
    positionVals = []
    markerVals = []
    directionVals = []

    for sub in subjects:
        for cond in conditions:
            data = optoData.loc[(optoData.subject == sub) & (optoData.condition == cond)]

            if len(data) == 0:
                print(cond + ' does not exist in ' + sub + 's file')
                continue
            else:
                print('working on ' + sub + ' ' + cond)
                position = pd.concat([data['Marker_1 x'],data['Marker_1 y'], data['Marker_1 z'],
                                      data['Marker_2 x'], data['Marker_2 y'], data['Marker_2 z'],
                                      data['Marker_3 x'], data['Marker_3 y'], data['Marker_3 z'],
                                      data['Marker_4 x'], data['Marker_4 y'], data['Marker_4 z'],
                                      data['Marker_5 x'], data['Marker_5 y'], data['Marker_5 z'],
                                      data['Marker_6 x'], data['Marker_6 y'], data['Marker_6 z'],
                                      data['Marker_7 x'], data['Marker_7 y'], data['Marker_7 z']])


                marker = pd.concat([pd.Series([1] * len(data['Marker_1 x']) * numDirections), pd.Series([2] * len(data['Marker_1 x']) * numDirections),
                                    pd.Series([3] * len(data['Marker_1 x']) * numDirections), pd.Series([4] * len(data['Marker_1 x']) * numDirections),
                                    pd.Series([5] * len(data['Marker_1 x']) * numDirections), pd.Series([6] * len(data['Marker_1 x']) * numDirections),
                                    pd.Series([7] * len(data['Marker_1 x']) * numDirections)])

                direction = pd.concat([pd.Series(['x'] * len(data['Marker_1 x'])), pd.Series(['y'] * len(data['Marker_1 y'])), pd.Series(['z'] * len(data['Marker_1 z']))])
                direction = pd.concat([direction] *numMarkers).to_list()

                time = pd.concat([data.Frame/samplingRate] *numMarkers *numDirections) # convert frame to time
                subList = pd.Series(np.hstack(([sub] * len(data['Marker_1 x']) *numMarkers *numDirections)))
                condList = pd.Series(np.hstack(([cond] * len(data['Marker_1 x']) *numMarkers *numDirections)))

                subVals.append(subList)
                condVals.append(condList)
                positionVals.append(position)
                markerVals.append(marker)
                directionVals.append(direction)
                timeVals.append(time)


    return subVals, condVals, timeVals, positionVals, markerVals, directionVals
subVals, condVals, timeVals, positionVals, markerVals, directionVals = makeOptoDF()

list_of_lists = [subVals, condVals, timeVals, positionVals, markerVals, directionVals]
flatL = makeFlatList(list_of_lists)

frames = {'subject': flatL[0], 'condition': flatL[1], 'time': flatL[2], 'position': flatL[3], 'marker': flatL[4], 'direction': flatL[5]}
df = pd.DataFrame(frames)

df.to_csv(data_dir + 'optoTidyDF.csv', index=False)