import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import sys

def read_and_plot(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith(("createWrite", "openRead", "rename")):
                parts = line.strip().split(',')
                operation = parts[0]
                timestamp = int(parts[1])
                duration = int(parts[2])
                data.append((operation, timestamp, duration))
    
    df = pd.DataFrame(data, columns=['operation', 'timestamp', 'duration'])
    
    start_time = df['timestamp'].min()
    df['relative_time'] = (df['timestamp'] - start_time) / 1000.0
    
    # df['formatted_time'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    plt.figure(figsize=(10, 6))
        
    lower_quantile = df['duration'].quantile(0.00)
    upper_quantile = df['duration'].quantile(0.99)
    df_filtered = df[(df['duration'] >= lower_quantile) & (df['duration'] <= upper_quantile)]    
    
    for operation in df_filtered['operation'].unique():
        subset = df_filtered[df_filtered['operation'] == operation]
        plt.plot(subset['relative_time'], subset['duration'], linestyle='-', label=operation)
    
    # plt.plot(df['relative_time'], df['duration'],linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Latency')
    plt.title('Latency vs Time')
    plt.grid(True)
    plt.ylim(bottom=0)
    plt.tight_layout()
    plt.savefig(filename + '.png')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    read_and_plot(filename)