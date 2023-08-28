import os
import pandas as pd
import numpy as np

# Create tidy version of the opto track data

eye_tracking = 1 # EyeSeeCam = 0; EyeLink = 1

# It's too large to send via Git. Make sure you download raw_data from the HU Box (ESC/recording_session_20220324)
#save_dir = r'C:/Users/angie/Box/EyeSeeCam/data/'

# Change directory and load optotrak and eye-tracking data
if eye_tracking == 0:
    data_dir = r'C:/Users/angie/Box/EyeSeeCam/data/esc_session/'
    os.chdir(data_dir)
elif eye_tracking == 1:
    data_dir = r'C:/Users/angie/Box/EyeSeeCam/data/eyeLink_session/'
    os.chdir(data_dir)

optoData = pd.read_csv('opto3_data.csv')

subjects = optoData.subject.unique()
conditions = optoData.condition.unique()
trials = optoData.trial.unique()
delays = optoData.delay.unique()
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
    delayVals = []
    trialVals = []
    timeVals = []
    positionVals = []
    markerVals = []
    directionVals = []

    for sub in subjects:
        for cond in conditions:
            for d in delays:
                for t in trials:

                    data = optoData.loc[(optoData.subject == sub) & (optoData.condition == cond) & (optoData.delay == d) & (optoData.trial == t)]

                    if len(data) == 0:
                        print('Subject: ' + sub + ' condition: ' + cond + ' delay: ' + str(d) + ' trial: ' + str(t) + ' does not exist')
                        continue
                    else:
                        print('working on subject: ' + sub + ', Condition: ' + cond + ', Delay: ' + str(d) + ' and Trial: ' + str(t))
                        position = pd.concat([data['Marker_1 x'], data['Marker_1 y'], data['Marker_1 z'],
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
                        delayList = pd.Series(np.hstack(([d] * len(data['Marker_1 x']) *numMarkers *numDirections)))
                        trialList = pd.Series(np.hstack(([t] * len(data['Marker_1 x']) * numMarkers * numDirections)))

                        subVals.append(subList)
                        condVals.append(condList)
                        delayVals.append(delayList)
                        trialVals.append(trialList)
                        positionVals.append(position)
                        markerVals.append(marker)
                        directionVals.append(direction)
                        timeVals.append(time)


    return subVals, condVals, delayVals, trialVals, timeVals, positionVals, markerVals, directionVals
subVals, condVals, delayVals, trialVals, timeVals, positionVals, markerVals, directionVals = makeOptoDF()

list_of_lists = [subVals, condVals, delayVals, trialVals, timeVals, positionVals, markerVals, directionVals]
flatL = makeFlatList(list_of_lists)

frames = {'subject': flatL[0], 'condition': flatL[1], 'delay':flatL[2], 'trial':flatL[3], 'time': flatL[4], 'position': flatL[5], 'marker': flatL[6], 'direction': flatL[7]}
df = pd.DataFrame(frames)

df.to_csv(data_dir + 'optoTidyDF.csv', index=False)