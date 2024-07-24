import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files, ignoring the last two rows
df_bindex = pd.read_csv(r"C:\Users\spachava\Downloads\M2_Stage_Energy_Opt_Code_Final_Files\Plot_Graph_Codes\Workload2\exe_times_WL2_BIndex.csv", encoding='utf-8').iloc[:-2]
df_aindex = pd.read_csv(r"C:\Users\spachava\Downloads\M2_Stage_Energy_Opt_Code_Final_Files\Plot_Graph_Codes\Workload2\exe_times_WL2_AIndex.csv", encoding='utf-8').iloc[:-2]

# Rename columns for clarity
df_bindex.rename(columns={'Execution_Time_ms': 'Execution_Time_BIndex(ms)'}, inplace=True)
df_aindex.rename(columns={'Execution_Time_ms': 'Execution_Time_AIndex(ms)'}, inplace=True)

# Merge the dataframes on 'Query_Number'
df = pd.merge(df_bindex, df_aindex, on='Query_Number')

# Plot the execution times
plt.figure(figsize=(12, 6))

# Plot Execution Time BIndex
plt.plot(df['Query_Number'], df['Execution_Time_BIndex(ms)'], label='Execution Time BIndex(ms)', marker='o')

# Plot Execution Time AIndex
plt.plot(df['Query_Number'], df['Execution_Time_AIndex(ms)'], label='Execution Time AIndex(ms)', marker='x')

# Add titles and labels
plt.title('Estimated Execution Time Comparison')
plt.xlabel('Query Number')
plt.ylabel('Execution Time (ms)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.legend()
plt.grid(True)

# Save the plot as a PNG file
plt.tight_layout()
plt.savefig('execution_time_comparisonWL1.png')

# Show the plot
plt.show()