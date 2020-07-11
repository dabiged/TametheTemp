# -*- coding: utf-8 -*-

##################################################################
# This file is used to generate your predictions. You may not    #
# need to change it however it lets you control how the pickle   #
# file is loaded.                                                #
##################################################################


import logging
import os

import pickle

from src.process import get_processed_data


def predict(raw_data_file, processed_data_folderpath, model_folderpath, output_filepath, model_name):
    logger = logging.getLogger(__name__)
    logger.info('Creating prediction using processed data and trained model')

    predict_df = get_processed_data(input_filepath=raw_data_file, output_folderpath=processed_data_folderpath,
                                    pipeline='predict')

    logger.info('Loading model')
    # Load in pickled trained model
    with open(os.path.join(model_folderpath, os.path.join(model_name, f'{model_name}.pkl')), 'rb') as pickle_file:
        regressor = pickle.load(pickle_file)

    logger.info('Predicting')
    # Make prediction
    prediction = regressor.predict(predict_df)
    predict_df['prediction'] = prediction

    logger.info('Saving predicted data')
    _save_predictions(output_filepath, predict_df)


def _save_predictions(output_filepath, predict_df):
    """Construct and save export"""
    output_df = predict_df[['prediction']]
    output_df.to_csv(output_filepath, index=None)
