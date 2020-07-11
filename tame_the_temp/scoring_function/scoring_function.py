# -*- coding: utf-8 -*-
"""This code is used for scoring. Note that any changes you make here will have no effect of the
score you get when your code is submitted"""


import logging
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error


def score(prediction_filepath, public_actual_filepath, private_actual_filepath, score_filepath):
    logger = logging.getLogger(__name__)
    logger.info('Calculating the model\'s SME score')

    # Run prediction data through scoring functions to produce a public and private score.
    # submission private scores will not be released until the end of the competition, and are
    # what is used to decide the competition winner.
    scores = _calculate_score(prediction_filepath, public_actual_filepath, private_actual_filepath)
    logger.info('Public Score: {}'.format(scores['public']))
    logger.info('Private Score: {}'.format(scores['private']))

    # Save the scores in JSON format.
    logger.info('Saving score')
    with open(score_filepath, 'w') as file:
        file.write('{{"public":{},"private":{}}}'.format(scores['public'], scores['private']))


def _calculate_score(submission_filepath, public_target_filepath, private_target_filepath):
    # Perform scoring here...
    logger = logging.getLogger(__name__)

    public_target = pd.read_csv(public_target_filepath)
    private_target = pd.read_csv(private_target_filepath)
    submission = pd.read_csv(submission_filepath)

    logger.info(f'score data sizes: {public_target.shape}, {private_target.shape}, {submission.shape}')
    logger.info(f'score data samples: {public_target.iloc[:10, 0]}, {private_target.iloc[:10, 0]}, {submission.iloc[:10, 0]}')

    public_submission_size = public_target.shape[0]

    return {
        'public': np.sqrt(mean_squared_error(public_target, submission[:public_submission_size])),
        'private': np.sqrt(mean_squared_error(private_target, submission[public_submission_size:])),
    }
