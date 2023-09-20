import pandas as pd
import matplotlib.pyplot as plt


def event_distribution(time_data: list, time_interval: str = '5T'):
    timestamps = pd.to_datetime(time_data)

    timestamps_series = pd.Series(timestamps)
    timestamps_series.index = timestamps
    event_counts = timestamps_series.groupby(pd.Grouper(freq=time_interval)).size()

    num_intervals = len(event_counts)
    display_points = 10
    display_interval = int(num_intervals / display_points)

    plt.figure(figsize=(10, 6))
    event_counts.plot(kind='bar')

    plt.xlabel('Time Interval')
    plt.ylabel('Event Count')
    plt.title('Event Counts by Time Interval')

    x_labels = [str(time.time().strftime('%H:%M')) for time in event_counts.index[::display_interval]]
    x_ticks = list(range(0, len(event_counts), display_interval))

    plt.xticks(x_ticks, x_labels, rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    plt.show()
