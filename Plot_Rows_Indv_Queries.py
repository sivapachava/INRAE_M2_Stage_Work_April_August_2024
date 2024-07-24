import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read CSV files
bindex_data = pd.read_csv(r"C:\Users\spachava\Downloads\M2_Stage_Energy_Opt_Code_Final_Files\Plot_Graph_Codes\Workload1\total_rows_before_index.csv")
aindex_data = pd.read_csv(r"C:\Users\spachava\Downloads\M2_Stage_Energy_Opt_Code_Final_Files\Plot_Graph_Codes\Workload1\total_rows_after_index.csv")

# Filter data for 'Total' rows only
bindex_total = bindex_data[bindex_data['Operator'] == 'Total']
aindex_total = aindex_data[aindex_data['Operator'] == 'Total']

# Extract relevant columns
queries = bindex_total['Query Number']  # Assuming both CSVs have the same query order

bindex_actual_before = bindex_total['Actual Rows BIndex']
aindex_actual_after = aindex_total['Actual Rows AIndex']

# Calculate bar positions
bar_width = 0.35  # Width of the bars
index = np.arange(len(queries))  # x-axis locations for the groups

# Plotting comparison between Actual Rows Before vs After Index
# Plotting comparison between Actual Rows Before vs After Index
plt.figure(figsize=(14, 7))

plt.bar(index - bar_width/2, bindex_actual_before, width=bar_width, label='Before Index', color='blue')
plt.bar(index + bar_width/2, aindex_actual_after, width=bar_width, label='After Index', color='orange', alpha=0.7)

plt.xlabel('Query Number', fontsize = 20)
plt.ylabel('Actual Rows', fontsize = 20)
plt.title('Actual Rows Before vs After Index Comparison', fontsize = 20)
plt.xticks(index, queries, fontsize = 16)
plt.yticks(fontsize=20)
#plt.legend()
legend = plt.legend(fontsize=15)
legend.set_title(legend.get_title().get_text(), prop={'size': 18})
plt.grid(False)  # Disable grid lines
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.tight_layout()

# Save and display the plot
plt.savefig('actual_rows_WL1.png')
plt.show()


bindex_planned_before = bindex_total['Planned Rows BIndex']
aindex_planned_after = aindex_total['Planned Rows AIndex']
# Plotting comparison between Planned Rows After vs Before Index
plt.figure(figsize=(14, 7))

plt.bar(index - bar_width/2, aindex_planned_after, width=bar_width, label='After Index', color='green')
plt.bar(index + bar_width/2, bindex_planned_before, width=bar_width, label='Before Index', color='red', alpha=0.7)

plt.xlabel('Query Number', fontsize = 20)
plt.ylabel('Planned Rows', fontsize = 20)
plt.title('Planned Rows After vs Before Index Comparison', fontsize = 20)
plt.xticks(index, queries, fontsize = 16)
plt.yticks(fontsize=20)
#plt.legend()
legend = plt.legend(fontsize=15)
legend.set_title(legend.get_title().get_text(), prop={'size': 18})
plt.grid(False)  # Disable grid lines
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.tight_layout()

# Save and display the plot
plt.savefig('planned_rows_WL1.png')
plt.show()
