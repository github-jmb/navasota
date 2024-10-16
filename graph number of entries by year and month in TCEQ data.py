import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

plt.ion()

directory = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(directory, 'swqmispublicdata.txt')

df = pd.read_csv(filepath, delimiter='|')
grouped = df.groupby('Station ID')
station_ids = list(grouped.groups.keys())
current_index = 0  

df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')
df['Year'] = df['End Date'].dt.year
df['Month'] = df['End Date'].dt.month

fig, ax = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(bottom=0.15, hspace=0.5)  

ax_next = plt.axes([0.9, 0.01, 0.08, 0.025])  
ax_prev = plt.axes([0.8, 0.01, 0.08, 0.025])  
button_next = Button(ax_next, 'Next')
button_prev = Button(ax_prev, 'Previous')

def plot_station_data(index):
    """Plot data for the specified station index."""
    station_id = station_ids[index]
    group = grouped.get_group(station_id)

    group = group.dropna(subset=['Year', 'Month'])

    for a in ax:
        a.cla()  

    yearly_activity = group['Year'].value_counts().sort_index()
    ax[0].bar(yearly_activity.index, yearly_activity.values)
    ax[0].set_title(f'Relative Activity by Year - Station {station_id}')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Number of Entries')

    monthly_activity = group['Month'].value_counts().sort_index()
    ax[1].bar(monthly_activity.index, monthly_activity.values,
            tick_label=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax[1].set_title(f'Total Number of Results by Month (Summed Over Time) - Station {station_id}')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Number of Entries')

    plt.tight_layout()
    plt.draw()

def next_station(event):
    global current_index
    current_index = (current_index + 1) % len(station_ids)
    plot_station_data(current_index)

def previous_station(event):
    global current_index
    current_index = (current_index - 1) % len(station_ids)
    plot_station_data(current_index)

plot_station_data(current_index)

button_next.on_clicked(next_station)
button_prev.on_clicked(previous_station)

plt.show(block=True)

