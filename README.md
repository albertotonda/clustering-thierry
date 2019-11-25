# clustering-thierry
Clustering experiments with Thierry Thomas-Danguin's data. 

# Chronicle for "clustering day"
In the beginning, data was 183 .csv files + one file with the meta-data.

# Notes

## 2019-11-25
- Normalize all time series
- Use Dynamic Time Warping to compute distance matrix between all time series
- Use Agglomerative Clustering as usual
- Choose a certain number of clusters
- Plot the time series in each cluster

TODO: pre-compute distance matrix (DTW is really slow)

## 2019-11-24
Look up Dynamic Time Warping, https://towardsdatascience.com/time-series-hierarchical-clustering-using-dynamic-time-warping-in-python-c8c9edf2fda5

## 2019-10-17
First step: write a script to aggregate all results in ONE dataset.
