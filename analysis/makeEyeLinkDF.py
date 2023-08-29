import os
import pandas as pd
import numpy as np

data_dir = r'C:/Users/angie/Box/EyeSeeCam/data/eyeLink_session/'
os.chdir(data_dir)

# Load opto track data
eyeLinkDF = pd.read_csv('eyeLink_data.csv')

subjects = eyeLinkDF.subject.unique()
conditions = eyeLinkDF.condition.unique()
delays = eyeLinkDF.delay.unique()
trials = eyeLinkDF.trial.unique()
numMarkers = 4
numDirections = 2
samplingRate = 250

sampleDifference = 0.004 # Sample at 250 Hz

# Function to make flat list
def makeFlatList(input_list):
    flatL = []

    for idx, itemL in enumerate(input_list):
        flat_list = [item for sublist in input_list[idx] for item in sublist]
        flatL.append(flat_list)

    return flatL

# Make tidy pandas data frame for Eye Link data
def makeEyeLinkDF():
    subVals = []
    condVals = []
    delayVals = []
    trialVals = []
    timeVals = []
    retrieveTimeVals = []
    positionVals = []
    markerVals = []
    directionVals = []
    ELTimeVals = []

    for sub in subjects:
        for cond in conditions:
            for d in delays:
                for t in trials:

                    data = eyeLinkDF.loc[(eyeLinkDF.subject == sub) & (eyeLinkDF.condition == cond) & (eyeLinkDF.delay == d) & (eyeLinkDF.trial == t)]

                    if len(data) == 0:
                        print('Subject: ' + sub + ' condition: ' + cond + ' delay: ' + str(d) + ' trial: ' + str(t) + ' does not exist')
                        continue
                    else:
                        print('working on subject: ' + sub + ', Condition: ' + cond + ', Delay: ' + str(
                            d) + ' and Trial: ' + str(t))

                    position = pd.concat([data['Marker1X'], data['Marker1Y'],
                                           data['Marker2X'], data['Marker2Y'],
                                           data['Marker3X'], data['Marker3Y'],
                                           data['Marker4X'], data['Marker4Y']])

                    marker = pd.concat([pd.Series([1] * len(data['Marker1X']) * numDirections), pd.Series([2] * len(data['Marker1X']) * numDirections),
                                        pd.Series([3] * len(data['Marker1X']) * numDirections), pd.Series([4] * len(data['Marker1X']) * numDirections)])

                    direction = pd.concat([pd.Series(['x'] * len(data['Marker1X'])), pd.Series(['y'] * len(data['Marker1X']))])
                    direction = pd.concat([direction] * numMarkers).to_list()

                    elTime = pd.concat([data.Time_EL] *numMarkers *numDirections)

                    data['Time_EL'] = (data['Time_EL'] - data['Time_EL'].iloc[0]) / 1000
                    data['RetrieveTime_EL'] = data['RetrieveTime_EL'] / 1000

                    time = pd.concat([data.Time_EL] *numMarkers *numDirections)
                    retrieve_time_EL = pd.concat([data.RetrieveTime_EL] *numMarkers *numDirections)

                    subList = pd.Series(np.hstack(([sub] * len(data['Marker1X']) *numMarkers *numDirections)))
                    condList = pd.Series(np.hstack(([cond] * len(data['Marker1X']) *numMarkers *numDirections)))
                    delayList = pd.Series(np.hstack(([d] * len(data['Marker1X']) *numMarkers *numDirections)))
                    trialList = pd.Series(np.hstack(([t] * len(data['Marker1X']) *numMarkers *numDirections)))

                    subVals.append(subList)
                    condVals.append(condList)
                    delayVals.append(delayList)
                    trialVals.append(trialList)
                    ELTimeVals.append(elTime)
                    timeVals.append(time)
                    retrieveTimeVals.append(retrieve_time_EL)
                    positionVals.append(position)
                    markerVals.append(marker)
                    directionVals.append(direction)

    return subVals, condVals, delayVals, trialVals, ELTimeVals, timeVals, retrieveTimeVals, positionVals, markerVals, directionVals
subVals, condVals, delayVals, trialVals, ELTimeVals, timeVals, retrieveTimeVals, positionVals, markerVals, directionVals = makeEyeLinkDF()

list_of_list = [subVals, condVals, delayVals, trialVals, ELTimeVals, timeVals, retrieveTimeVals, positionVals, markerVals, directionVals]
flatL = makeFlatList(list_of_list)

frames = {'subject':flatL[0], 'condition':flatL[1], 'delay':flatL[2], 'trial':flatL[3], 'Time_EL':flatL[4], 'frameTime':flatL[5], 'retrieveTime':flatL[6], 'position':flatL[7], 'marker':flatL[8], 'direction':flatL[9]}
df = pd.DataFrame(frames)

df.to_csv(data_dir + 'elTidyDF.csv', index=False)