import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data preparation
data_workload2_energy = {
    'Metric': ['mWh Workload1', 'mWh Workload2'],
    'Run 1': [871.8, 711.6],
    'Run 2': [736.2, 677.6]
}

data_workload2_time = {
    'Metric': ['sec Workload1', 'sec Workload2'],
    'Run 1': [134.69, 105.408],
    'Run 2': [132.43, 90.342]
}

# Create dataframes
df_workload2_energy = pd.DataFrame(data_workload2_energy)
df_workload2_time = pd.DataFrame(data_workload2_time)

# Function to plot grouped bar chart with value labels
def plot_grouped_bar_chart(df, workload_name, metric):
    n_groups = len(df['Metric'])
    fig, ax = plt.subplots(figsize=(10, 6))

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.8

    rects1 = plt.bar(index, df['Run 1'], bar_width, alpha=opacity, color='b', label='Before Index')
    rects2 = plt.bar(index + bar_width, df['Run 2'], bar_width, alpha=opacity, color='g', label='After Index')

    plt.xlabel(' ')
    plt.ylabel(f'{metric} Values')
    plt.title(f'{workload_name} {metric} Comparison')
    plt.xticks(index + bar_width / 2, df['Metric'], rotation=0, ha='center')
    plt.legend()

    # Add value labels on top of the bars
    for i in range(len(rects1)):
        ax.text(rects1[i].get_x() + rects1[i].get_width() / 2., rects1[i].get_height(),
                f'{df["Run 1"][i]}', ha='center', va='bottom')
        ax.text(rects2[i].get_x() + rects2[i].get_width() / 2., rects2[i].get_height(),
                f'{df["Run 2"][i]}', ha='center', va='bottom')

    plt.grid(False)  # Disable grid lines
    plt.tight_layout()
    plt.savefig(f'{workload_name}_{metric}_grouped_bar_comparison.png')
    plt.show()

# Plot grouped bar charts for energy consumption
plot_grouped_bar_chart(df_workload2_energy, 'workload2', 'Energy Consumption(mWh)')

# Plot grouped bar charts for execution time
plot_grouped_bar_chart(df_workload2_time, 'workload2', 'Execution Time(sec)')
