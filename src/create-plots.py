# Script to aggregate all Thierry's data into one dataset
# by Alberto Tonda, 2019 <alberto.tonda@gmail.com>

import matplotlib.pyplot as plt
import os
import pandas as pd
import sys

def main() :

    # a few hard-coded values
    folder = "../data"
    meta_data_file = os.path.join(folder, "Metadonnées.xlsx")
    column_file = 'CSV file'
    column_product = 'Name of product'
    column_ion = 'Ion'
    column_repetition = 'Repetition'
    
    output_folder = "plots"
    if not os.path.exists(output_folder) : os.makedirs(output_folder)

    # start by reading the meta-data file
    print("Reading %s..." % meta_data_file)
    df = pd.read_excel(meta_data_file, sheet_name='Feuil1')

    # we get the unique values for product and ion
    unique_products = df[column_product].unique()
    unique_ions = df[column_ion].unique()

    for product in unique_products :
        for ion in unique_ions :
            
            df_selection = df[ (df[column_product] == product) & (df[column_ion] == ion) ]
            print("For product %s, ion %s, we have %d lines" % (product, ion, len(df_selection)))

            # plot something only if we actually found experiments for that combination of product and ion
            if len(df_selection) > 0 :
                file_names = df_selection[column_file].unique()
                rep_names = df_selection[column_repetition].unique()

                fig = plt.figure()
                ax = fig.add_subplot(111)
                min_length = 0

                for index, file_name in enumerate(file_names) :
                    df_experiment = pd.read_csv( os.path.join(folder, file_name), sep=';' )
                    all_data = df_experiment.values

                    ax.plot(all_data[:,0], all_data[:,2], label="Repetition %d" % rep_names[index])
                    if all_data.shape[0] > min_length : min_length = all_data.shape[0]

                ax.legend(loc='best')
                ax.set_title("Product %s, Ion %s (%d entries)" % (product, ion, min_length))
                ax.set_ylabel("Intensity")
                ax.set_xlabel("Time")
                plt.savefig( os.path.join(output_folder, "%s-%s.pdf" % (ion, product)) )
                plt.close(fig)


    return

if __name__ == "__main__" :
    sys.exit( main() )
