import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data preparation
data_workloads_energy = {
    'Metric': ['Workload1', 'Workload2',  'Workload3'],
    'Before Index': [2143.8, 852.8, 1440.6],
    'After Index':  [1598.6, 840.8, 1783.4]
}

data_workloads_time = {
    'Metric': ['Workload1', 'Workload2', 'Workload3'],
    'Before Index': [281.62, 193.84, 157.04],
    'After Index':  [256.70, 170.88, 193.14]
}

# Create dataframes
df_workloads_energy = pd.DataFrame(data_workloads_energy)
df_workloads_time = pd.DataFrame(data_workloads_time)

# Function to plot grouped bar chart with value labels
def plot_grouped_bar_chart(df, workload_name, metric):
    n_groups = len(df['Metric'])
    fig, ax = plt.subplots(figsize=(10, 6))

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.8

    rects1 = plt.bar(index, df['Before Index'], bar_width, alpha=opacity, color='b', label='Before Index')
    rects2 = plt.bar(index + bar_width, df['After Index'], bar_width, alpha=opacity, color='g', label='After Index')

    plt.xlabel(' ', fontsize = 20)
    plt.ylabel(f'{metric} Values', fontsize = 20)
    plt.title(f'{workload_name} {metric} Comparison', fontsize = 20)
    plt.xticks(index + bar_width / 2, df['Metric'], rotation=0, ha='center', fontsize = 20)
    plt.yticks(fontsize=20)
    #plt.legend()
    legend = plt.legend(fontsize=15, loc='upper right')
    legend.set_title(legend.get_title().get_text(), prop={'size': 15})

    # Add value labels on top of the bars
    for i in range(len(rects1)):
        ax.text(rects1[i].get_x() + rects1[i].get_width() / 2., rects1[i].get_height(),
                f'{df["Before Index"][i]}', ha='center', va='bottom', fontsize = 16)
        ax.text(rects2[i].get_x() + rects2[i].get_width() / 2., rects2[i].get_height(),
                f'{df["After Index"][i]}', ha='center', va='bottom', fontsize = 16)

    plt.grid(False)  # Disable grid lines
    plt.tight_layout()
    plt.savefig(f'{workload_name}_{metric}_comparison.png')
    plt.show()

# Plot grouped bar charts for energy consumption
plot_grouped_bar_chart(df_workloads_energy, 'workloads', 'Energy Consumption(mWh)')

# Plot grouped bar charts for execution time
plot_grouped_bar_chart(df_workloads_time, 'workloads', 'Execution Time(sec)')
