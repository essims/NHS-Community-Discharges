# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 13:44:38 2023

@author: Esra Simsek
"""

import pandas as pd
import string
from datetime import datetime, timedelta


# Read the CSV file from the website
df = pd.read_excel(r"C:\Users\Esra Simsek\Desktop\Community Discharge\Community discharge-November 2023\Community-discharge-sitrep-monthly-data-webfile-November2023.xlsx", sheet_name='Table 2')



df.columns = [''] * len(df.columns)


#Delete the first 2 columns
df = df.iloc[:, 2:]


def generate_column_names(num_columns):
    columns = []
    letters = list(string.ascii_uppercase)  # Get all uppercase letters as a list
    
    # Generate names using a combination of letters and numbers
    for i in range(num_columns):
        col_name = ""
        
        # Add letter(s) to the column name
        col_name += letters[i // 10]  # First letter from A to Z
        col_name += letters[i % 10]   # Second letter from A to Z
        
        # Add a number to the column name
        col_name += str((i % 100) // 10)   # Tens digit of the number
        col_name += str(i % 10)             # Units digit of the number
        
        columns.append(col_name)
    
    return columns

# Generate column names
column_names = generate_column_names(len(df.columns))



df.columns=column_names


def delete_data_before_value(df, column_name, search_value):
    # Find the index of the row containing the search value
    index = df.index[df[column_name] == search_value].tolist()[0]

    # Select the subset of the dataframe starting from the row with the search value
    df = df.iloc[index+1:]

    return df


search_value = 'Org Code'
column_name = 'AA00'

df = delete_data_before_value(df, column_name, search_value)
#df.to_csv("cleaning2.csv", index=False)

length=len(df)


# Hold the first 2 columns
first_three_columns = df.iloc[:, :2]

# Unpivot the remaining columns
df = df.melt(id_vars=first_three_columns.columns.tolist())

old_variable_name1 = 'AC02',  'AF05',  'AI08',  'BB11',  'BE14',  'BH17','CA20',  'CD23', 'CG26',  'CJ29',  'DC32',  'DF35',  'DI38',  'EB41',  'EE44','EH47',  'FA50', 'FD53', 'FG56',  'FJ59',  'GC62', 'GF65',  'GI68',  'HB71','HE74',  'HH77',  'IA80','ID83',  'IG86',  'IJ89', 'JC92'
       
new_variable_name1 = 'Number of patients who no longer meet the criteria to reside'

# Replace the old variable name with the new variable name in the column
df['variable'] = df['variable'].replace(old_variable_name1, new_variable_name1)


old_variable_name2 =  'AD03',  'AG06', 'AJ09',  'BC12',  'BF15', 'BI18',  'CB21',  'CE24', 'CH27',  'DA30',  'DD33', 'DG36', 'DJ39',  'EC42','EF45',  'EI48',  'FB51',  'FE54',  'FH57',  'GA60', 'GD63', 'GG66', 'GJ69',  'HC72',  'HF75',  'HI78',  'IB81',  'IE84',  'IH87', 'JA90', 'JD93'
new_variable_name2 = 'Number of patients discharged '

# Replace the old variable name with the new variable name in the column
df['variable'] = df['variable'].replace(old_variable_name2, new_variable_name2)


old_variable_name3 = 'AE04', 'AH07', 'BA10',  'BD13',  'BG16', 'BJ19',  'CC22',  'CF25', 'CI28',  'DB31',  'DE34', 'DH37',  'EA40',  'ED43',  'EG46',  'EJ49',  'FC52',  'FF55',  'FI58',  'GB61', 'GE64',  'GH67',  'HA70',  'HD73', 'HG76',  'HJ79',  'IC82', 'IF85',  'II88', 'JB91', 'JE94'
new_variable_name3 = 'Number of patients remaining in hospital who no longer meet the criteria to reside'

# Replace the old variable name with the new variable name in the column
df['variable'] = df['variable'].replace(old_variable_name3, new_variable_name3)


# Define the mapping dictionary for column name changes
column_mapping = {'AA00': 'Code', 'AB01': 'Name', 'variable': 'Criteria'}

# Rename the columns
df.rename(columns=column_mapping, inplace=True)


# Set the start and end dates
start_date = datetime(2023, 11, 1)
end_date = datetime(2023,11,30)

# Create a list to store the dates
dates = []

# Define the number of repetitions for each date
repetitions = length*3

# Generate the dates and repetitions
current_date = start_date
while current_date <= end_date:
    dates.extend([current_date] * repetitions)
    current_date += timedelta(days=1)

# Create a dataframe
Date = pd.DataFrame({'Date': dates})

df['date']=Date

# Replace '-' values with NaN
df['value'] = pd.to_numeric(df['value'], errors='coerce')

 
# Filter data for the desired criteria
filtered_df = df[df['Criteria'] == 'Number of patients remaining in hospital who no longer meet the criteria to reside']

# Group by 'Item' column and calculate the average
grouped = filtered_df.groupby(['Code','Name'])['value'].mean().reset_index()

# Merge the 'Code' and 'Name' columns with a '-' separator and store them in a new column 'Code-Name'
grouped['Code-Name'] = grouped['Code'].astype(str) + '-' + grouped['Name']

# Categorize avg_value into 3 groups
grouped['performance_group'] = pd.qcut(grouped['value'], q=4, labels=['The best performers', 'The good performers','The bad performers', 'The worst performers'])


# Filter performers based on performance groups
best_performers_list = grouped[grouped['performance_group'] == 'The best performers']['Code-Name'].tolist()
good_performers_list = grouped[grouped['performance_group'] == 'The good performers']['Code-Name' ].tolist()
bad_performers_list = grouped[grouped['performance_group'] == 'The bad performers']['Code-Name'].tolist()
worst_performers_list = grouped[grouped['performance_group'] == 'The worst performers']['Code-Name'].tolist()


# Ensure all lists have the same length
max_length = max(len(best_performers_list),len(good_performers_list), len(bad_performers_list), len(worst_performers_list))
best_performers_list.extend([''] * (max_length - len(best_performers_list)))
good_performers_list.extend([''] * (max_length - len(good_performers_list)))
bad_performers_list.extend([''] * (max_length - len(bad_performers_list)))
worst_performers_list.extend([''] * (max_length - len(worst_performers_list)))

# Save performers lists to a CSV file
performers_df = pd.DataFrame({
    'Best Performers': best_performers_list,
    'Good Performers': good_performers_list,
    'Bad Performers': bad_performers_list,
    'Worst Performers': worst_performers_list
})



file_path= "C:\\Users\\Esra Simsek\\Desktop\\Community Discharge\\Community discharge-November 2023\\Performers-November23.csv"

performers_df.to_csv(file_path, index=False)

