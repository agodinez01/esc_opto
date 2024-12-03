# esc_opto
To validate EyeSeeCam head sensors by co-registering the system with Optotrak and EyeLink 1000+

1. createInitDF.py takes in individual files EyeSee Cam (ESC) and Opto track data and stacks them all together to get a DF of all data.
    - Creates csv files: esc_data.csv, opto3_data.csv and opto6_data.csv
2. makeOptoDF.py makes tidy DF for opto track data for each marker and direction (x, y, z)
    - Creates optoTidyDF.csv
3. 
