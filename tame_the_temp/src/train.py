# -*- coding: utf-8 -*-

import logging
import os
from pathlib import Path

import pickle
from sklearn.linear_model import LinearRegression

from src.process import get_processed_data


def train(raw_data_file, processed_data_folderpath, model_folderpath, model_name):
    logger = logging.getLogger(__name__)
    logger.info('Training model with processed data')

    x_train_df, y_train_df = get_processed_data(raw_data_file, processed_data_folderpath, pipeline='train')

    # This is a place holder for a model. Replace this with you model.
    regressor = LinearRegression(n_jobs=-1)
    print("Training a linear Regressor")

    logger.info('Training model')
    regressor.fit(x_train_df, y_train_df.values[:, 0])

    logger.info('Saving model')
    _save_model(model_folderpath, model_name, regressor)


def _save_model(model_folderpath, model_name, regressor):
    """This"""
    model_folderpath = os.path.join(model_folderpath, model_name)
    Path(model_folderpath).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(model_folderpath, f'{model_name}.pkl'), 'wb') as pickle_file:
        pickle.dump(regressor, pickle_file)
