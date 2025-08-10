"""
Created on Wed Dec 17 15:18:13 2024

@author: Una Drayton
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

IMPORT_FILE = r'Substation load 6-2024.csv'
DATE = 'June 2024'
CURRENT_PEAK = 4.9
FUTURE_PEAK = 5.2
CONTROLLABLE_LOAD_MVA = 1.102 / 10 # Controllable Load at Substation / No. Control Channels
THRESHOLD_MVA = 4.8
ADD_THRESHOLD_MVA = THRESHOLD_MVA - 0.1 # Threshold that load must drop below before reconnecting load
CAPACITY_MVA = 5 # Substation N-1 security limit


CHANNELS_ENGAGED = 0
LOAD_DROPPED = 0

# Funciton that inputs a load value and reduces by set amount until below threshold
def drop_load(curr_load, threshold, add_threshold, control_amount):
    global CHANNELS_ENGAGED 
    global LOAD_DROPPED #keeps track of how many channels we have to put back on 
    # If load is above threshold drop load until below or no. of channels runs out
    
    print('Real load = ', curr_load)
    
    new_load = curr_load - CHANNELS_ENGAGED * control_amount
    # print('Load due to channels = ', new_load)
    
    
    if new_load > threshold:
        # print('DROPPING------------------------------')
        while (new_load > float(threshold)) and (CHANNELS_ENGAGED < 10):
            CHANNELS_ENGAGED += 1
            new_load -= control_amount
        print('Channels engaged = ', CHANNELS_ENGAGED)
        print('Load to drop = ', LOAD_DROPPED)
    # Otherwise return dropped load - staggered
    elif new_load < add_threshold:
        if CHANNELS_ENGAGED > 0:
            # print('ADDING+++++++++++++++++++++++++++++++++++')
            CHANNELS_ENGAGED -= 1
            new_load += control_amount
        
        if (LOAD_DROPPED > 0) and (CHANNELS_ENGAGED == 0):
            while (LOAD_DROPPED > 0) and (new_load < add_threshold):
                LOAD_DROPPED -= 1
                new_load += control_amount
        
    LOAD_DROPPED += CHANNELS_ENGAGED
                        
    return new_load


df = pd.read_csv(IMPORT_FILE, index_col='Time Bin')
df['Proportional Peak Load'] = df/df.max()
df['Current Peak Load'] = df['Proportional Peak Load'] * CURRENT_PEAK
df['Future Peak Load'] = df['Proportional Peak Load'] * FUTURE_PEAK
# Apply load control
df['Controlled Load (Current)'] = df['Current Peak Load'].apply(lambda x: drop_load(x, THRESHOLD_MVA, ADD_THRESHOLD_MVA, CONTROLLABLE_LOAD_MVA))
df['Controlled Load (Future)'] = df['Future Peak Load'].apply(lambda x: drop_load(x, THRESHOLD_MVA, ADD_THRESHOLD_MVA, CONTROLLABLE_LOAD_MVA))
df['Proportional Controlled Load'] = df['Controlled Load (Future)']/df['Future Peak Load'].max()

# Plotting for predicted (future) peak load
fig, ax = plt.subplots(figsize=(10, 6))
plt.plot(df['Future Peak Load'], 'go-', label='Uncontrolled Peak Load')
plt.plot(df['Controlled Load (Future)'], 'bo-', label='Controlled Load')
plt.axhline(CAPACITY_MVA, color='r', linestyle='--', label='Network Capacity')
plt.axhline(THRESHOLD_MVA, color='orange', linestyle='--', label='Control Threshold')

# Plotting for current peak load 
# fig, ax = plt.subplots(figsize=(10, 6))
# plt.plot(df['Current Peak Load'], 'o-', color='purple', label='Current')
# plt.plot(df['Controlled Load (Current)'], 'bo-', label='Controlled (Current)')
# plt.plot(df['Proportional Controlled Load']* FUTURE_PEAK, 'yo-', label='Controlled Load')

# Recorded average profile for mogiven month
# plt.plot(df['Total Load'], color='purple', linestyle='--', label='June 2024 Average Daily Load Profile')

# Calculate time labels (in hours and minutes) for each Time Bin
time_labels = np.arange(0, 2400, 100) # label every hour
time_labels_str = [f'{str(label).zfill(4)[:2]}:{str(label).zfill(4)[2:]}' for label in time_labels]

plt.xticks(np.arange(0, 96, 4), time_labels_str, rotation = 60)

# plt.title(DATE + ' Peak Load Profile at Substation')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Load (MVA)')
ax.set_xlim(0, 96)
# ax.set_ylim(0, 5.5)
plt.legend()
plt.grid()
