import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from scipy.stats import gmean
import matplotlib.pyplot as plt
import seaborn as sns

# A quick pass to assess whether we are getting a relatively good signal from the EyeSee Cam head sensors.

# Change data_dir to where your repository lives and save_dir to wherever your data will live (I usually have it in the cloud since it't too big to GitHub).
data_dir = r'C:/Users/angie/Box/EyeSeeCam/data/' # It's too large to send via Git. Make sure you download raw_data from the HU Box (ESC/recording_session_20220324)
#save_dir = r'C:/Users/angie/Box/EyeSeeCam/data/'

# Change directory and load optotrak and eyeSeeCam data
os.chdir(data_dir)

escData = pd.read_csv('esc_data.csv')
optoData = pd.read_csv('opto3_data.csv')

subjects = escData.subject.unique()
condition = escData.condition.unique()

# Function to make flat list
def makeFlatList(input_list):
    flatL = []

    for idx, itemL in enumerate(input_list):
        flat_list = [item for sublist in input_list[idx] for item in sublist]
        flatL.append(flat_list)

    return flatL

# Create DF for variables of interest
def createESC_HeadSensorDF():
    subVals = []
    conditionVals = []
    timeVals = []
    timeSourceVals = []
    headInertialVals = []
    sensorDircetionVals = []
    calibVals = []
    typeVals = []

    for sub in subjects:
        for cond in condition:

            subCondData = escData.loc[(escData.subject == sub) & (escData.condition == cond)]

            if len(subCondData) == 0:
                print(cond + ' does not exist in ' + sub + 's file')
                continue

            else:
                print('working on ' + sub + ' ' + cond)

                headInertial = pd.concat([subCondData.HeadInertialAccelX, subCondData.HeadInertialAccelY, subCondData.HeadInertialAccelZ,
                                          subCondData.HeadInertialAccelXCal, subCondData.HeadInertialAccelYCal, subCondData.HeadInertialAccelZCal,

                                          subCondData.HeadInertialMagX, subCondData.HeadInertialMagY, subCondData.HeadInertialMagZ,
                                          subCondData.HeadInertialMagXCal, subCondData.HeadInertialMagYCal, subCondData.HeadInertialMagZCal,

                                          subCondData.HeadInertialVelX, subCondData.HeadInertialVelY, subCondData.HeadInertialVelZ,
                                          subCondData.HeadInertialVelXCal, subCondData.HeadInertialVelYCal, subCondData.HeadInertialVelZCal,
                                          ])

                headInertial = pd.concat([headInertial, headInertial, headInertial]).to_list()
                print(len(headInertial))

                sensorDirectionList = pd.Series(np.hstack((['x'] * len(subCondData.HeadInertialAccelX),
                                             ['y'] * len(subCondData.HeadInertialAccelY),
                                             ['z'] * len(subCondData.HeadInertialAccelZ))))

                sensorDirection = pd.concat([sensorDirectionList] * 18).to_list()

                calibList = pd.Series(np.hstack((['uncalibrated'] * len(subCondData.HeadInertialAccelX) * 3, ['calibrated'] * len(subCondData.HeadInertialAccelX) * 3)))
                calib = pd.concat([calibList] * 9).to_list()

                typeList = pd.Series(np.hstack((['accel'] * len(subCondData.HeadInertialAccelX) * 6, ['mag'] * len(subCondData.HeadInertialAccelX) * 6, ['vel'] * len(subCondData.HeadInertialAccelX) * 6)))
                type = pd.concat([typeList] *3).to_list()

                retrieve_timeList = pd.concat([subCondData.RetrieveTime] *18)
                left_timeLisr = pd.concat([subCondData.LeftSystemTime] *18)
                right_timeList = pd.concat([subCondData.RightSystemTime] *18)

                time = pd.Series(np.hstack((retrieve_timeList, left_timeLisr, right_timeList))).to_list()

                retrieve_timeSourceList = pd.Series(np.hstack((['RetrieveTime'] * len(subCondData.RetrieveTime) * 18)))
                left_timeSourceLisr = pd.Series(np.hstack((['LeftSystemTime'] * len(subCondData.LeftSystemTime) * 18)))
                right_timeSourceList = pd.Series(np.hstack((['RightSystemTime'] * len(subCondData.RightSystemTime) * 18)))

                timeSource = pd.Series(np.hstack((retrieve_timeSourceList, left_timeSourceLisr, right_timeSourceList))).to_list()

                subList = pd.Series(np.hstack(([sub] * len(subCondData.RetrieveTime) * 54))).to_list()
                condList = pd.Series(np.hstack(([cond] * len(subCondData.RetrieveTime) * 54))).to_list()

                subVals.append([subList])
                conditionVals.append([condList])
                timeVals.append([time])
                timeSourceVals.append([timeSource])
                headInertialVals.append([headInertial])
                sensorDircetionVals.append([sensorDirection])
                calibVals.append([calib])
                typeVals.append([type])

    return subVals, conditionVals, timeVals, timeSourceVals, headInertialVals, sensorDircetionVals, calibVals, typeVals
subVals, conditionVals, timeVals, timeSourceVals, headInertialVals, sensorDirectionVals, calibVals, typeVals = createESC_HeadSensorDF()

list_of_lists = [subVals, conditionVals, timeVals, timeSourceVals, headInertialVals, sensorDirectionVals, typeVals, calibVals]
flatL = makeFlatList(list_of_lists)

frames = {'subject': flatL[0], 'condition': flatL[1], 'time': flatL[2], 'time_source': flatL[3], 'head_inertial_values':flatL[4], 'sensor_direction': flatL[5], 'sensor_data_type': flatL[6], 'calib': flatL[7]}
df = pd.DataFrame(frames)

df.to_csv(data_dir + 'escDataFrame.csv', index=False)