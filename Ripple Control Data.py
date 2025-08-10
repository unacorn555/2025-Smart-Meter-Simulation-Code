"""
Created on Mon Jan  6 15:18:05 2025

@author: UnaDrayton

Inputs a df of load data for one day taken at 15min interval (96 data points) 
and prints one graph showing daily profile.  
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import ceil

#Global Values
POWER_CONVERSION = (11000/(3**(1/2))) / 1000000
# Indexes of control periods
CONTROL_START_INDEX_1 = 30
CONTROL_END_INDEX_1 = 35
CONTROL_START_INDEX_2 = 68
CONTROL_END_INDEX_2 = 83


# source file which you has the column headings you want to find in the files you want to edit
source_filename = r'Zone Substaiton Load Control Event 20.07.24'


df = pd.read_csv(source_filename+'.csv', index_col=False)
df_avg = pd.read_csv(r'Substation load 6-2024.csv', index_col=False)

df['Total Current'] = (df['Current A_x'] + df['Current B_x'] + df['Current C_x'] + df['Current A_y'] + df['Current B_y'] + df['Current C_y'] + df['Current A'] + df['Current B'] + df['Current C'])
df_out = df.copy()

df_out['Total Load'] = df_out['Total Current'] * POWER_CONVERSION

# Calculate time labels (in hours and minutes) for each Time Bin
time_labels = [(bin * 15) // 60 * 100 + (bin * 15) % 60 for bin in df_out.index]
# Adjust x-axis ticks to display every 30 minutes
tick_positions = [i for i in range(0, 96, 4)]  # Every 2 data points corresponds to 30 minutes
# Convert to a readable time format (e.g., 00:00, 00:15, 00:30, ...)
time_labels_str = [f'{str(time_labels[i]).zfill(4)[:2]}:{str(time_labels[i]).zfill(4)[2:]}' for i in tick_positions]

   

fig, ax = plt.subplots()
plt.plot(df_out['Total Load'], marker='o', linestyle='-', label='Observed Load Profile')
plt.plot(df_avg['Total Load'], marker='o', linestyle='-', label='Monthly Average Profile')

# Set x-ticks to the time labels
plt.xticks(tick_positions, time_labels_str, rotation=60)  # Rotating for readability
ax.set_xlim(0,96)

# Plot load control periods 
plt.axvspan(CONTROL_START_INDEX_1, CONTROL_END_INDEX_1, color='y', alpha=0.5, lw=0, label='Control Period')
plt.axvspan(CONTROL_START_INDEX_2, CONTROL_END_INDEX_2, color='y', alpha=0.5, lw=0)

# Adding labels and title
plt.xlabel('Time (HH:MM)')
plt.ylabel('Load (MVA)')
plt.title(source_filename)

plt.legend()
plt.grid()
plt.show()
