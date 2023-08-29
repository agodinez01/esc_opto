import os
from os import listdir
from os.path import isfile, join
import pandas as pd

# Created by A. Godinez April 2022
# Takes in data from EyeSeeCam, merges it into one pd dataframe and saves as csv file. Does the same for optotrak data.
# 24/08/2023 Added code for EyeLink run.

# Change data_dir to where your repository lives and save_dir to wherever your data will live (I usually have it in the cloud since it't too big to GitHub).
data_dir = r'C:/Users/angie/Box/EyeSeeCam/raw_data/' # For EyeSeeCam, it's too large to send via Git. Make sure you download raw_data from the HU Box (ESC/recording_session_20220324)

# Then run. Should work.

eye_tracking = 1 # EyeSeeCam = 0; EyeLink = 1

if eye_tracking == 0:
    save_dir = r'C:/Users/angie/Box/EyeSeeCam/data/esc_session/'
elif eye_tracking == 1:
    save_dir = r'C:/Users/angie/Box/EyeSeeCam/data/eyeLink_session/'

# Load optotrak and eye tracking data
os.chdir(data_dir)

# Go through every folder in the path and create a list
a = [x[0] for x in os.walk(data_dir)]
system_list = [f for f in listdir(data_dir)]

def get_csv_file():

    data_eye = []
    data_opto3d = []
    data_opto6d = []

    for sys in system_list:
        file_dir = data_dir + sys
        os.chdir(file_dir)

        sys_file_list = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]

        for file in sys_file_list:
            df = []

            if sys == 'esc':
                df = pd.read_csv(file_dir + '/' + file, index_col=False)
                df['start_stamp'] = file[8:28]

                if file[0:2] == 'ba':
                    df['subject'] = file[0:4]
                    df['condition'] = 'still'

                else:
                    df['subject'] = file[0:2]
                    df['condition'] = file[2:5]

                data_eye.append(df)

            elif sys == 'optotrak':
                df = pd.read_csv(file_dir + '/' + file, skiprows=3, index_col=False)
                if file[32:34] == '3d':
                    data_opto3d.append(df)

                elif file[32:34] == '6d':
                    data_opto6d.append(df)

                if file[-9:-7] == 'ba':
                    df['subject'] = file[-9:-5]
                    df['condition'] = 'still'

                else:
                    df['subject'] = file[-9:-7]
                    df['condition'] = file[-7:-4]

            elif sys == 'optotrak2':
                df = pd.read_csv(file_dir + '/' + file, skiprows=3, index_col=False)
                assert len(df) == 8750, f"Expected a length of 8750, but got something else {len(df)}"

                if file[32:34] == '3d':
                    data_opto3d.append(df)

                elif file[32:34] == '6d':
                    data_opto6d.append(df)

                df['subject'] = file[-12:-10]
                df['trial'] = file[-10]
                df['condition'] = file[-9:-6]
                df['delay'] = file[-5]

            elif sys == 'eyeLink':
                df = pd.read_csv(file_dir + '/' + file, index_col=False)
                assert len(df) == 8750, f"Expected a length of 8750, but got something else {len(df)}"


                df['start_stamp'] = file[9:29]
                df['subject'] = file[0:2]
                df['trial'] = file[2]
                df['condition'] = file[3:6]
                df['delay'] = file[7]

                data_eye.append(df)

    return data_eye, data_opto3d, data_opto6d

if eye_tracking == 0:
    data_eye, data_opto3d, data_opto6d = get_csv_file()

    esc_data = pd.concat(data_eye)
    esc_data['condition'].replace({'0': 'still', 0: 'still'})
    esc_data.to_csv(save_dir + 'esc_data.csv', index=False)

elif eye_tracking == 1:
    data_eye, data_opto3d, data_opto6d = get_csv_file()

    eyeLink_data = pd.concat(data_eye)
    eyeLink_data.to_csv(save_dir + 'eyeLink_data.csv', index=False)

opto3_data = pd.concat(data_opto3d)
opto3_data.to_csv(save_dir + 'opto3_data.csv', index=False)

opto6_data = pd.concat(data_opto6d)
opto6_data.to_csv(save_dir + 'opto6_data.csv', index=False)