##################################################################
# This file provides a data loading function that will also work #
# on the industry partners pipeline. It's aware of the data      #
# folder structure, exactly as it's loaded from the data lake.   #
##################################################################

import pandas as pd
from pathlib import Path

def load_data(data_path):
    """
    Parameters
    ----------
    data_path: str
    Returns
    -------
    pandas.DataFrame
    """
    df = pd.DataFrame()
    training_data_path = Path(data_path)
    data_folders = [file for file in training_data_path.iterdir()
                    if file.is_dir() and file.name[:12] == 'month_start=']
    # each folder in extract contains a month worth of data
    for folder in data_folders:
        # each data file is in .csv format
        data_files = [file for file in folder.iterdir()
                      if file.is_file() and file.name[-4:] == '.csv']
        # read each individual file and save to a data frame
        for file in data_files:
            df_temp = pd.read_csv(file,
                                  index_col="timestamp",
                                  parse_dates=True)
            df = pd.concat([df, df_temp])
    # ensure a consistent column order
    df = df.reindex(sorted(df.columns), axis=1)
    return df.sort_values('timestamp')
