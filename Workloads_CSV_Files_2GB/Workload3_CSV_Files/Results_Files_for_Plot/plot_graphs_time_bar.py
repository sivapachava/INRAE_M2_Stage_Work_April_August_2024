import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV files
# Assuming the files have exactly 17 query results with headers
df_bindex = pd.read_csv(r"C:\Users\spachava\Downloads\M2_Stage_Energy_Opt_Code_Final_Files\Plot_Graph_Codes\Workload3\exe_times_WL3_BIndex.csv", encoding='utf-8')
df_aindex = pd.read_csv(r"C:\Users\spachava\Downloads\M2_Stage_Energy_Opt_Code_Final_Files\Plot_Graph_Codes\Workload3\exe_times_WL3_AIndex.csv", encoding='utf-8')

# Rename columns for clarity
df_bindex.rename(columns={'Execution_Time_ms': 'Execution_Time_BIndex(ms)'}, inplace=True)
df_aindex.rename(columns={'Execution_Time_ms': 'Execution_Time_AIndex(ms)'}, inplace=True)

# Merge the dataframes on 'Query_Number'
df = pd.merge(df_bindex, df_aindex, on='Query_Number')

# Plot the execution times as a grouped bar chart
plt.figure(figsize=(12, 6))

# Define bar width
bar_width = 0.35

# Define the positions of the bars
bar1 = np.arange(len(df['Query_Number']))
bar2 = [x + bar_width for x in bar1]

# Plot Execution Time BIndex
plt.bar(bar1, df['Execution_Time_BIndex(ms)'], width=bar_width, label='Before Index(ms)')

# Plot Execution Time AIndex
plt.bar(bar2, df['Execution_Time_AIndex(ms)'], width=bar_width, label='After Index(ms)')

# Add titles and labels
plt.title('Estimated Execution Time Comparison Workload3', fontsize = 20)
plt.xlabel('Query Number', fontsize = 20)
plt.ylabel('Execution Time (ms)', fontsize = 20)
plt.xticks([r + bar_width / 2 for r in range(len(df['Query_Number']))], df['Query_Number'], rotation=45, fontsize=20)
plt.yticks(fontsize=20)
#plt.legend()
legend = plt.legend(fontsize=20)
legend.set_title(legend.get_title().get_text(), prop={'size': 23})
plt.grid(False)

# Save the plot as a PNG file
plt.tight_layout()
plt.savefig('execution_time_comparisonWL3.png')

# Show the plot
plt.show()
