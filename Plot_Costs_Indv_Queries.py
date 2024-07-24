import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read CSV data into DataFrames
before_index_df = pd.read_csv(r"C:\Users\spachava\Downloads\M2_Stage_Energy_Opt_Code_Final_Files\Plot_Graph_Codes\Workload1\total_costs_before_index.csv")
after_index_df = pd.read_csv(r"C:\Users\spachava\Downloads\M2_Stage_Energy_Opt_Code_Final_Files\Plot_Graph_Codes\Workload1\total_costs_after_index.csv")

# Extract total initial and final costs
queries = [f'Q{i}' for i in range(1, 21)]

# Get initial and final costs for before index
total_initial_cost_bindex = before_index_df[before_index_df['Query_Number'].str.contains('Total Initial Cost')]['Cost_BIndex'].astype(float).reset_index(drop=True)
total_final_cost_bindex = before_index_df[before_index_df['Query_Number'].str.contains('Total Final Cost')]['Cost_BIndex'].astype(float).reset_index(drop=True)

# Get initial and final costs for after index
total_initial_cost_aindex = after_index_df[after_index_df['Query_Number'].str.contains('Total Initial Cost')]['Cost_AIndex'].astype(float).reset_index(drop=True)
total_final_cost_aindex = after_index_df[after_index_df['Query_Number'].str.contains('Total Final Cost')]['Cost_AIndex'].astype(float).reset_index(drop=True)

# Calculate bar positions
bar_width = 0.35  # Width of the bars
index = np.arange(len(queries))  # x-axis locations for the groups

# Plot grouped bar chart for initial costs
plt.figure(figsize=(14, 7))
plt.bar(index - bar_width/2, total_initial_cost_bindex, bar_width, label='Before Index')
plt.bar(index + bar_width/2, total_initial_cost_aindex, bar_width, label='After Index')
plt.xlabel('Queries', fontsize = 20)
plt.ylabel('Total Initial Cost', fontsize = 20)
plt.title('Total Initial Cost Before and After Index', fontsize = 20)
plt.xticks(index, queries, fontsize = 16)
plt.yticks(fontsize=20)
#plt.legend()
legend = plt.legend(fontsize=15)
legend.set_title(legend.get_title().get_text(), prop={'size': 18})
plt.grid(False)  # Disable grid lines
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.tight_layout()
plt.savefig('initial_costs_WL1.png')
plt.show()

# Plot grouped bar chart for final costs
plt.figure(figsize=(14, 7))
plt.bar(index - bar_width/2, total_final_cost_bindex, bar_width, label='Before Index')
plt.bar(index + bar_width/2, total_final_cost_aindex, bar_width, label='After Index')
plt.xlabel('Queries', fontsize = 20)
plt.ylabel('Total Final Cost', fontsize = 20)
plt.title('Total Final Cost Before and After Index', fontsize = 20)
plt.xticks(index, queries, fontsize = 16)
plt.yticks(fontsize=20)
#plt.legend()
legend = plt.legend(fontsize=15)
legend.set_title(legend.get_title().get_text(), prop={'size': 18})
plt.grid(False)  # Disable grid lines
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.tight_layout()
plt.savefig('final_costs_WL1.png')
plt.show()