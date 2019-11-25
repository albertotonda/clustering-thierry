import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import scipy.cluster.hierarchy as shc

from dtaidistance import dtw
from tslearn.preprocessing import TimeSeriesScalerMeanVariance
from tslearn import metrics

# prepare dataset with all time series
print("Loading/creating dataset...")
time_series = []
time_series_names = []

# a few hard-coded values
folder = "../data"
meta_data_file = os.path.join(folder, "Metadonnées.xlsx")
column_file = 'CSV file'

# start by reading the meta-data file
print("Reading %s..." % meta_data_file)
df = pd.read_excel(meta_data_file, sheet_name='Feuil1')

# some useful values, to be computed
min_len_time_series = np.inf
max_len_time_series = 0
n_time_series = 0

# iterate over the lines
for index, row in df.iterrows() :

    print("Reading row #%d, file: \"%s\"" % (index, row[column_file]))
    
    # read the file name written in the row
    df_experiment = pd.read_csv( os.path.join(folder, row[column_file]), sep=';' )
    len_of_trajectory = len(df_experiment)
    print("The file has %d lines" % len_of_trajectory)

    # update variables
    n_time_series += 1
    if len_of_trajectory > max_len_time_series : 
        max_len_time_series = len(df_experiment)
    elif len_of_trajectory < min_len_time_series : 
        min_len_time_series = len(df_experiment)

    #time_series.append( [ [v] for v in df_experiment.iloc[:,2].values.tolist() ] )
    time_series.append( df_experiment.iloc[:,2].values.tolist() )
    time_series_names.append( row[column_file].split('.')[0] )

print("Preparing data...")
scaler = TimeSeriesScalerMeanVariance(mu=0., std=1.) # rescale time series
time_series_scaled = scaler.fit_transform(time_series)

print("Computing Dynamic Time Warping distance matrix...")
distance_matrix = np.zeros((n_time_series, n_time_series))

for i in range(0, n_time_series) :
    for j in range(0, n_time_series) :
        if i != j :
            print("Computing distance time series #%d - #%d" % (i, j))
            # this is the tslearn version of DTW, that was creating memory errors
            #path, distance = metrics.dtw_path(time_series_scaled[i], time_series_scaled[j])
            # this is the dtaidistance version of DTW
            distance = dtw.distance(time_series_scaled[i], time_series_scaled[j], psi=1)

            distance_matrix[i, j] = distance
        
# now, let's call our clustering algorithms, with a pre-computed distance matrix
plt.figure(figsize=(10, 7))
plt.title("Dendrograms")
dend = shc.dendrogram(shc.linkage(time_series_scaled, method='ward', metric=lambda u, v : distance_matrix(u, v)))
plt.axhline(y=cutoff_distance, color='r', linestyle='--')
plt.savefig( os.path.join(folder_name, "hierarchical-dendogram.pdf") )
