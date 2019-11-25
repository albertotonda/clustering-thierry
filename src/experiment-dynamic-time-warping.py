import os
import pandas as pd
import random
from copy import deepcopy
from scipy import interpolate
import numpy as np
from dtaidistance import dtw
import matplotlib.pyplot as plt
from _plotly_future_ import v4_subplots
import plotly.graph_objects as go
from plotly.subplots import make_subplots

print("Loading/creating dataset...")

# a few hard-coded values
folder = "../data"
meta_data_file = os.path.join(folder, "Metadonnées.xlsx")
column_file = 'CSV file'

# start by reading the meta-data file
print("Reading %s..." % meta_data_file)
df = pd.read_excel(meta_data_file, sheet_name='Feuil1')

# variables that are later used by the clustering process
NUM_OF_TRAJECTORIES = 0
MIN_LEN_OF_TRAJECTORY = 30000
MAX_LEN_OF_TRAJECTORY = -1
THRESHOLD = 0.50

# dictionary that will contain all the time series/trajectories
trajectoriesSet = dict()

# iterate over the lines
for index, row in df.iterrows() :

    print("Reading row #%d, file: \"%s\"" % (index, row[column_file]))
    
    # read the file name written in the row
    df_experiment = pd.read_csv( os.path.join(folder, row[column_file]), sep=';' )
    len_of_trajectory = len(df_experiment)
    print("The file has %d lines" % len_of_trajectory)

    # update variables
    NUM_OF_TRAJECTORIES += 1
    if len_of_trajectory > MAX_LEN_OF_TRAJECTORY : 
        MAX_LEN_OF_TRAJECTORY = len(df_experiment)
    elif len_of_trajectory < MIN_LEN_OF_TRAJECTORY : 
        MIN_LEN_OF_TRAJECTORY = len(df_experiment)
    
    # debugging
    print(df_experiment)

    # store trajectory in dictionary; the trajectory is stored in the second column, as a list, because the following algorithm needs it
    trajectoriesSet[ (str(index,)) ] = df_experiment.iloc[:,2].values.tolist() 


print("NUM_OF_TRAJECTORIES=%d, MAX_LEN_OF_TRAJECTORY=%d, MIN_LEN_OF_TRAJECTORY=%d" % (NUM_OF_TRAJECTORIES, MAX_LEN_OF_TRAJECTORY, MIN_LEN_OF_TRAJECTORY))

# TODO normalize range of each trajectory?

print("Clustering...")

trajectories = deepcopy(trajectoriesSet)
distanceMatrixDictionary = {}
iteration = 1
while True:
   distanceMatrix = np.empty((len(trajectories), len(trajectories),))
   distanceMatrix[:] = np.nan
   
   for index1, (filter1, trajectory1) in enumerate(trajectories.items()):
      tempArray = []
      
      for index2, (filter2, trajectory2) in enumerate(trajectories.items()):
         
         if index1 > index2:
            continue
         
         elif index1 == index2:
            continue
         
         else:
            unionFilter = filter1 + filter2
            sorted(unionFilter)
            
            if unionFilter in distanceMatrixDictionary.keys():
               distanceMatrix[index1][index2] = distanceMatrixDictionary.get(unionFilter)
               
               continue
            
            metric = []
            for subItem1 in trajectory1:
               
               for subItem2 in trajectory2:
                  metric.append(dtw.distance(subItem1, subItem2, psi=1))
            
            metric = max(metric)
            
            distanceMatrix[index1][index2] = metric
            distanceMatrixDictionary[unionFilter] = metric

