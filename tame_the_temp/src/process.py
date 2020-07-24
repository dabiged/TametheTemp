# -*- coding: utf-8 -*-

import logging
import os
import numpy as np
import pandas as pd
from src.industry import load_data


def process(input_filepath, output_folderpath, pipeline):
    get_processed_data(input_filepath, output_folderpath, pipeline)


def get_processed_data(input_filepath, output_folderpath, pipeline):
    logger = logging.getLogger(__name__)
    logger.info('Making processed data set from raw data')
    # Read in data from csv
    df = load_data(input_filepath).reset_index()

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # We have put some simple data processing here. Additional data processing can be added here.
    logger.info('Cleaning the raw data')
    strings_to_replace = ['I/O Timeout', 'Bad Input', 'Over Range', 'Under Range', 'Arc Off-line']
    df = df.replace(strings_to_replace, np.nan)

    data_columns = list(df.columns)
    if pipeline == 'train':
        # drop rows containing null/nan values
        df = df[df[data_columns].notnull().all(axis=1)]
    else:
        df.fillna(0.0, inplace=True)

    firstACcolsList=['timestamp', 'PPO:AC4_1A:TIC7201-PV', 'PPO:AC4_1A:FIC7201-PV', 'PPO:AC4_1A:FIC7271-PV', 'PPO:AC4_1A:WIC7211-PV', 'PPO:PU2033:FI7061', 'PPO:PU2034:FI7062', 'PPO:PU2035:FI7063', 'PPO:PU2033:WI7061', 'PPO:PU2034:WI7062', 'PPO:PU2035:WI7063', 'PPO:PU2033:WIC7064-PV', 'PPO:PU2741:TIC7182-PV', 'PPO:L-AC4 FD_S2_2HR_SQL', 'PPO:L-AC4FD_RS_2HR_SQL', 'PPO:L-AC4 FD_CACO3_2HR_SQL', 'PPO:L-AC4 FD_PH_2HR_SQL', 'PPO:AG2241:JIC7201-PV', 'PPO:AG2241:AG2241-RPM', 'PPO:AC2004:PIC7065A-PV', 'PPO:PV2016:PV7127', 'PPO:PV2017:PV7137', 'PPO:AC2004:LIC7280-PV', 'PPO:PV2004:ZI7121', 'PPO:PV2005:ZI7131', 'PPO:PV2004:FIC7121-PV', 'PPO:PV2005:FIC7131-PV', 'PPO:L-AC4_S2_2HR_SQL', 'PPO:L-ACD4_ORP_3HR_SQL', 'PPO:L-ACD4_H2SO4_3HR_SQL']
    for col in df.columns:
        if col not in firstACcolsList:
            df.drop(col,axis=1,inplace=True)
    logger.info('Dropping NonAC1 columns')
    # Write data to csv files
    logger.info('Saving processed data')
    output = _save_processed_data(df, output_folderpath, pipeline)
    logger.info('Finished processing data')
    return output


def _save_processed_data(df, output_folderpath, pipeline):
    """This is a required step. This function should be unchanged."""
    if pipeline == 'train':
        x_df, y_df = _extract_y_value(df)

        y_df.to_csv(os.path.join(output_folderpath, 'y_train.csv'), index=False)
        x_df.to_csv(os.path.join(output_folderpath, 'x_train.csv'), index=False)
        return x_df, y_df
    else:
        df = df.drop(columns=['timestamp'])
        df.to_csv(os.path.join(output_folderpath, 'predict.csv'), index=False)
        return df


def _extract_y_value(df):
    """The target or y-value here is the field PPO:AC4_1A:TIC7201-PV, lagged by one hour.
    This should probably be left unchanged."""
    x_columns = df.columns.values.tolist()
    df['target_timestamp'] = df['timestamp'] - pd.Timedelta(seconds=3600)
    df['target_PPO:AC4_1A:TIC7201-PV'] = df['PPO:AC4_1A:TIC7201-PV']
    x_df = df[x_columns]
    y_df = df[['target_timestamp', 'target_PPO:AC4_1A:TIC7201-PV']]
    merged_df = pd.merge(x_df, y_df, left_on='timestamp', right_on='target_timestamp')
    x_df = merged_df[x_columns].drop(columns=['timestamp'])
    y_df = merged_df[['target_PPO:AC4_1A:TIC7201-PV']].rename(columns={
        'target_PPO:AC4_1A:TIC7201-PV': 'PPO:AC4_1A:TIC7201-PV'
    })
    return x_df, y_df
