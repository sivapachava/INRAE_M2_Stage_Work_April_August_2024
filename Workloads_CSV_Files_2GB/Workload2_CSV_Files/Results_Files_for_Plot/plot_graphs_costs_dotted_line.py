import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read CSV data into DataFrames
before_index_df = pd.read_csv(r"C:\Users\spachava\Downloads\M2_Stage_Work_Code_Files\Final_Files\Workload2_CSV_Files\query_Tcosts_WL2_BIndex_for_graph.csv")
after_index_df = pd.read_csv(r"C:\Users\spachava\Downloads\M2_Stage_Work_Code_Files\Final_Files\Workload2_CSV_Files\query_Tcosts_WL2_AIndex_for_graph.csv")

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
plt.bar(index - bar_width/2, total_initial_cost_bindex, bar_width, label='Before Index - Initial Cost')
plt.bar(index + bar_width/2, total_initial_cost_aindex, bar_width, label='After Index - Initial Cost')
plt.xlabel('Queries')
plt.ylabel('Total Initial Cost')
plt.title('Total Initial Cost Before and After Index')
plt.xticks(index, queries)
plt.legend()
plt.grid(True, which='both', linestyle='--')
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.tight_layout()
plt.savefig('initial_costs_comparison_1.png')
plt.show()

# Plot grouped bar chart for final costs
plt.figure(figsize=(14, 7))
plt.bar(index - bar_width/2, total_final_cost_bindex, bar_width, label='Before Index - Final Cost')
plt.bar(index + bar_width/2, total_final_cost_aindex, bar_width, label='After Index - Final Cost')
plt.xlabel('Queries')
plt.ylabel('Total Final Cost')
plt.title('Total Final Cost Before and After Index')
plt.xticks(index, queries)
plt.legend()
plt.grid(True, which='both', linestyle='--')
plt.yscale('log')  # Set y-axis to logarithmic scale
plt.tight_layout()
plt.savefig('final_costs_comparison_1.png')
plt.show()