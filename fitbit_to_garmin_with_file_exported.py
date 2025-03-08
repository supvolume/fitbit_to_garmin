"""
Convert data export from Fitbit into csv that can be imported to Garmin
The data that can be import are as follow:
1. Body: weight in fitbit export as lbs and will get converted to kg
2. Activities: there might be timezone different in datetime data. Please recheck if it crucial.
3. Calories Burned
4. Steps
5. Distance: export data from Fitbit is in cm and will get converted to km
6. Floors: altitude, every 10 altitude = 1 floor
7. Minutes Sedentary
8. Minutes Lightly Active
9. Minutes Fairly Active
10. Minutes Very Active

Activity Calories: Data is not listed as importable.

Please double check data unit

Large dataset may be too large to import, please adjust "number of export files" parameter
"""

import os
import json
import csv
import pandas as pd

# file path
dir_path = '{file path here}'
save_file_name = 'fitbit_export_combine'

# number of export files
number_of_export_files = 2

# Fitbit data that want to be import
import_activity = ['weight',
                   'calories',
                   'steps',
                   'distance',
                   'altitude',
                   'sedentary_minutes',
                   'lightly_active_minutes',
                   'moderately_active_minutes',
                   'very_active_minutes']


dataframes = []


# Activity
for activity in import_activity:
    if activity == 'weight':

    ## Body
        dfs_temp = []
        json_files = [f for f in os.listdir(dir_path+'/Personal & Account/') if (f.endswith('.json')) and (f.startswith('weight'))]
        for f in json_files:
            df_temp = pd.read_json(dir_path+'/Personal & Account/'+f)
            dfs_temp.append(df_temp)

        body_df = pd.concat(dfs_temp, ignore_index=True)
        body_df['weight'] = (body_df['weight']*0.45359237).round(1) # convert lbs to kg
        body_df = body_df.fillna(0)
        body_df['fat'] = body_df['fat'].astype('int64')
        body_df_fin = body_df[['date','weight','bmi','fat']]
        body_df_fin.columns = ['Date','Weight','BMI','Fat']


        # for adjust number of export files
        total_row = body_df_fin.shape[0]
        bin_size = total_row // number_of_export_files
        n_beginning = 0
        n_end = bin_size+(total_row%number_of_export_files)


        # Create file and write body data
        for i in range(number_of_export_files):
            with open(save_file_name+'_'+str(i)+'.csv', 'w', newline='\n') as csvfile:
                csvfile.write('Body\n')

            with open(save_file_name+'_'+str(i)+'.csv', 'a', newline='\n') as csvfile:
                body_df_fin.iloc[n_beginning:n_end].to_csv(save_file_name+'_'+str(i)+'.csv', mode='a', header=True, index=False)

            n_beginning = n_end
            n_end = n_end + bin_size


    ## Activity data
    else:
        dfs_temp = []
        json_files = [f for f in os.listdir(dir_path+'/Physical Activity/') if (f.endswith('.json')) and (f.startswith(activity))]
        for f in json_files:
            df_temp = pd.read_json(dir_path+'/Physical Activity/'+f)
            dfs_temp.append(df_temp)

        dfs_concat = pd.concat(dfs_temp, ignore_index=True)

        dfs_concat['Date'] = dfs_concat['dateTime'].dt.date
        dfs_concat['Time'] = dfs_concat['dateTime'].dt.date

        dfs_concat = dfs_concat[['Date','value']].groupby('Date').sum().reset_index()

        # Calories Burned
        if activity == 'calories':
            calories_df = dfs_concat
            calories_df['value'] = calories_df['value'].round(0).astype('int64')
            calories_df.columns = ['Date', 'Calories Burned']
            dataframes.append(calories_df)

        # Steps
        elif activity == 'steps':
            steps_df = dfs_concat
            steps_df['value'] = steps_df['value'].round(0).astype('int64')
            steps_df.columns = ['Date', 'Steps']
            dataframes.append(steps_df)

        # Distance
        elif activity == 'distance':
            distance_df = dfs_concat
            distance_df['value'] = (distance_df['value']/100000).round(2)
            distance_df.columns = ['Date', 'Distance']
            dataframes.append(distance_df)

        # Floor
        elif activity == 'altitude':
            altitude_df = dfs_concat
            altitude_df['value'] = (altitude_df['value']/10).round(0).astype('int64')
            altitude_df.columns = ['Date', 'Floors']
            dataframes.append(altitude_df)

        # Minutes Sedentary
        elif activity == 'sedentary_minutes':
            sedentary_df = dfs_concat
            sedentary_df.columns = ['Date', 'Minutes Sedentary']
            dataframes.append(sedentary_df)

        # Minutes Lightly Active
        elif activity == 'lightly_active_minutes':
            lightly_active_df = dfs_concat
            lightly_active_df.columns = ['Date', 'Minutes Lightly Active']
            dataframes.append(lightly_active_df)

        # Minutes Fairly Active
        elif activity == 'moderately_active_minutes':
            moderately_active_df = dfs_concat
            moderately_active_df.columns = ['Date', 'Minutes Fairly Active']
            dataframes.append(moderately_active_df)

        # Minutes Very Active
        elif activity == 'very_active_minutes':
            very_active_df = dfs_concat
            very_active_df.columns = ['Date', 'Minutes Very Active']
            dataframes.append(very_active_df)

# Table for activity
activity_df = dataframes[0]
for df in dataframes[1:]:
    activity_df = activity_df.merge(df, on='Date',how='outer')
activity_df['Activity Calories'] = 0    # Data can't be import to Garmin
activity_df = activity_df.fillna(0)


# for adjust number of export files
total_row = activity_df.shape[0]
bin_size = total_row // number_of_export_files
n_beginning = 0
n_end = bin_size+(total_row%number_of_export_files)


# Write activity into csv
for i in range(number_of_export_files):
    with open(save_file_name+'_'+str(i)+'.csv', 'a', newline='\n') as csvfile:
        csvfile.write('\nActivities\n')

    with open(save_file_name+'_'+str(i)+'.csv', 'a', newline='\n') as csvfile:
        activity_df.iloc[n_beginning:n_end].to_csv(save_file_name+'_'+str(i)+'.csv', mode='a', header=True, index=False)

    n_beginning = n_end
    n_end = n_end + bin_size

