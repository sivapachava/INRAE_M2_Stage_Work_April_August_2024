import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data parsing
data_workload1_costs_rows = {
    #'Metric': ['Overall Total Initial Cost', 'Overall Total Final Cost', 'Overall Total Planned Rows', 'Overall Total Actual Rows'],
    'Metric': ['IC', 'FC', 'PR', 'AR'],
    'Run 1': [62091904.84, 82126214.75, 226190743, 182939369],
    'Run 2': [55541186.78, 74735644.45, 213340932, 177240843]
}

data_workload1_time = {
    'Metric': ['WL1 Time'],
    'Run 1': [274649.781],
    'Run 2': [241464.022]
}

data_workload2_costs_rows = {
    'Metric': ['IC', 'FC', 'PR', 'AR'],
    'Run 1': [22983357.16, 4137741351.81, 60770175161, 50624635],
    'Run 2': [17755838.59, 4129529305.66, 60765343059, 48302489]
}

data_workload2_time = {
    'Metric': ['WL2 Time'],
    'Run 1': [182044.707],
    'Run 2': [180167.975]
}

data_workload3_costs_rows = {
    'Metric': ['IC', 'FC', 'PR', 'AR'],
    'Run 1': [11513378.04, 28969633.44, 251925, 17738506],
    'Run 2': [11513361.85, 28969284.54, 251897, 17738670]
}

data_workload3_time = {
    'Metric': ['WL3 Time'],
    'Run 1': [94241.814],
    'Run 2': [94855.184]
}

# Create dataframes
df_workload1_costs_rows = pd.DataFrame(data_workload1_costs_rows)
df_workload1_time = pd.DataFrame(data_workload1_time)
df_workload2_costs_rows = pd.DataFrame(data_workload2_costs_rows)
df_workload2_time = pd.DataFrame(data_workload2_time)
df_workload3_costs_rows = pd.DataFrame(data_workload3_costs_rows)
df_workload3_time = pd.DataFrame(data_workload3_time)

# Function to plot grouped bar chart
def plot_grouped_bar_chart(df, workload_name, graph_type, log_scale=False):
    n_groups = len(df['Metric'])
    fig, ax = plt.subplots(figsize=(14, 8))

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.8

    rects1 = plt.bar(index, df['Run 1'], bar_width, alpha=opacity, color='b', label='Before Index')
    rects2 = plt.bar(index + bar_width, df['Run 2'], bar_width, alpha=opacity, color='g', label='After Index')

    plt.xlabel(' ', fontsize=24)
    plt.ylabel('Values', fontsize=20)
    plt.title(f'{workload_name} {graph_type} Comparison', fontsize=20)
    plt.xticks(index + bar_width / 2, df['Metric'], rotation=0, ha='center', fontsize=20)
    #plt.yticks(fontsize=20)
    #plt.legend()


    #plt.xlabel(' ', fontweight='bold')
    #plt.ylabel('Values', fontweight='bold')
    #plt.title(f'{workload_name} {graph_type} Comparison', fontweight='bold')
    #plt.xticks(index + bar_width / 2, df['Metric'], rotation=0, ha='center', fontweight='bold')
    
    #legend = plt.legend(fontsize='large', prop={'weight': 'bold'})
    #legend.set_title(legend.get_title().get_text(), prop={'size': '13', 'weight': 'bold'})
    
    legend = plt.legend(fontsize=22)
    legend.set_title(legend.get_title().get_text(), prop={'size': 23})

    if log_scale:
        ax.set_yscale('log')
    ax.tick_params(axis='y', labelsize=22, width=2)

    plt.tight_layout()
    plt.grid(False)
    plt.savefig(f'{workload_name}_{graph_type}_grouped_bar_comparison.png')
    plt.show()

# Plot grouped bar charts for workload1 costs and rows with log scale
plot_grouped_bar_chart(df_workload1_costs_rows, 'workload1', 'Costs and Rows', log_scale=True)

# Plot grouped bar charts for workload1 time
plot_grouped_bar_chart(df_workload1_time, 'workload1', 'Execution Time')

# Plot grouped bar charts for workload2 costs and rows with log scale
plot_grouped_bar_chart(df_workload2_costs_rows, 'workload2', 'Costs and Rows', log_scale=True)

# Plot grouped bar charts for workload2 time
plot_grouped_bar_chart(df_workload2_time, 'workload2', 'Execution Time')

# Plot grouped bar charts for workload1 costs and rows with log scale
plot_grouped_bar_chart(df_workload3_costs_rows, 'workload3', 'Costs and Rows', log_scale=True)

# Plot grouped bar charts for workload1 time
plot_grouped_bar_chart(df_workload3_time, 'workload3', 'Execution Time')
