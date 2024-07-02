
from matplotlib.lines import lineStyles
import pandas as pd
import matplotlib.pyplot as plt
#
#def read_data_from_csv (file_path, column_name):
#   
#    df = pd.read_csv(file_path)
#    
#    time_data = df[column_name].tolist()
#    return time_data

#print(data_to_plot)
#print(len(data_to_plot))

def plot_data(data_to_plot):
    
    labels = ['MySQL', 'Redis', 'Cache']
    x = range(len(data_to_plot))
    
    plt.figure(figsize=(10,5))
    plt.plot(data_to_plot, marker='o', linestyle='-')
    plt.title("Time taken to store data")
    plt.xlabel('Index')
    plt.ylabel('Time')
    plt.grid(True)
    
    plt.xticks(x, labels)
    plt.legend()
    
    plt.show()

data_to_plot = [0.11562347412109375, 0.42389512062072754, 0.004254579544067383]
#file_path = '/home/rafael/Desktop/url_uuid_v2/get_result_cache.csv'
#column_name = 'time'
#data_to_plot = read_data_from_csv(file_path, column_name)
print(len(data_to_plot))
plot_data(data_to_plot)