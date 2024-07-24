import pandas as pd

# Define the data for each workload
data_workload1_costs_rows = {
    'Metric': ['Total Initial Cost', 'Total Final Cost', 'Total Planned Rows', 'Total Actual Rows'],
    'Run 1': [62091904.84, 82126214.75, 226190743, 182939369],
    'Run 2': [55541186.78, 74735644.45, 213340932, 177240843]
}

data_workload1_time = {
    'Metric': ['Total Exe Time'],
    'Run 1': [274649.781],
    'Run 2': [241464.022]
}

data_workload2_costs_rows = {
    'Metric': ['Total Initial Cost', 'Total Final Cost', 'Total Planned Rows', 'Total Actual Rows'],
    'Run 1': [22983357.16, 4137741351.81, 60770175161, 50624635],
    'Run 2': [17755838.59, 4129529305.66, 60765343059, 48302489]
}

data_workload2_time = {
    'Metric': ['Total Exe Time'],
    'Run 1': [182044.707],
    'Run 2': [180167.975]
}

data_workload3_costs_rows = {
    'Metric': ['Total Initial Cost', 'Total Final Cost', 'Total Planned Rows', 'Total Actual Rows'],
    'Run 1': [11513378.04, 28969633.44, 251925, 17738506],
    'Run 2': [11513361.85, 28969284.54, 251897, 17738670]
}

data_workload3_time = {
    'Metric': ['Total Exe Time'],
    'Run 1': [94241.814],
    'Run 2': [94855.184]
}

# Convert the data into DataFrames
df_workload1_costs_rows = pd.DataFrame(data_workload1_costs_rows)
df_workload1_time = pd.DataFrame(data_workload1_time)

df_workload2_costs_rows = pd.DataFrame(data_workload2_costs_rows)
df_workload2_time = pd.DataFrame(data_workload2_time)

df_workload3_costs_rows = pd.DataFrame(data_workload3_costs_rows)
df_workload3_time = pd.DataFrame(data_workload3_time)

# Calculate the differences between Run 1 and Run 2
df_workload1_costs_rows['Difference'] = df_workload1_costs_rows['Run 1'] - df_workload1_costs_rows['Run 2']
df_workload1_time['Difference'] = df_workload1_time['Run 1'] - df_workload1_time['Run 2']

df_workload2_costs_rows['Difference'] = df_workload2_costs_rows['Run 1'] - df_workload2_costs_rows['Run 2']
df_workload2_time['Difference'] = df_workload2_time['Run 1'] - df_workload2_time['Run 2']

df_workload3_costs_rows['Difference'] = df_workload3_costs_rows['Run 1'] - df_workload3_costs_rows['Run 2']
df_workload3_time['Difference'] = df_workload3_time['Run 1'] - df_workload3_time['Run 2']

# Combine all differences into one table
combined_costs_rows = pd.DataFrame({
    'Metric': df_workload1_costs_rows['Metric'],
    'Workload 1': df_workload1_costs_rows['Difference'],
    'Workload 2': df_workload2_costs_rows['Difference'],
    'Workload 3': df_workload3_costs_rows['Difference']
})

combined_time = pd.DataFrame({
    'Metric': df_workload1_time['Metric'],
    'Workload 1': df_workload1_time['Difference'],
    'Workload 2': df_workload2_time['Difference'],
    'Workload 3': df_workload3_time['Difference']
})

# Find the maximum difference for each metric
combined_costs_rows['Max Difference'] = combined_costs_rows[['Workload 1', 'Workload 2', 'Workload 3']].max(axis=1)
combined_costs_rows['Max Workload'] = combined_costs_rows[['Workload 1', 'Workload 2', 'Workload 3']].idxmax(axis=1)

combined_time['Max Difference'] = combined_time[['Workload 1', 'Workload 2', 'Workload 3']].max(axis=1)
combined_time['Max Workload'] = combined_time[['Workload 1', 'Workload 2', 'Workload 3']].idxmax(axis=1)

# Display the combined tables with max differences
print("Combined Costs and Rows Differences:")
print(combined_costs_rows)

print("\nCombined Execution Time Differences:")
print(combined_time)
