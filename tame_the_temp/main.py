##################################################################
# This file is used as the entry point from our Makefile and     #
# should not be changed.                                         #
##################################################################

import argparse
import logging

from src.train import train
from src.predict import predict
from src.process import process

def main():
    args = _parse_args()
    args.func(args)

def _run_training(args):
    train(raw_data_file=args.raw_data_file, processed_data_folderpath=args.processed_data_folderpath,
          model_folderpath=args.model_folderpath, model_name=args.model_name)

def _run_processing(args):
    process(input_filepath=args.input_filepath, output_folderpath=args.output_folderpath, pipeline=args.pipeline)

def _run_prediction(args):
    predict(
        raw_data_file=args.raw_data_file,
        processed_data_folderpath=args.processed_data_folderpath,
        model_folderpath=args.model_folderpath,
        output_filepath=args.output_filepath,
        model_name=args.model_name
    )

def _parse_args():
    parser = argparse.ArgumentParser('Predict')
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help')
    subparsers.required = True
    subparsers.dest = 'command'

    process_parser = subparsers.add_parser('process')

    process_parser.add_argument(
        '--input_filepath',
        type=str,
        help="Path to the data that is being processed",
        required=True
    )

    process_parser.add_argument(
        '--output_folderpath',
        type=str,
        help="Same as the input_folderpath for the train and predict scripts",
        required=True
    )

    process_parser.add_argument(
        '--pipeline',
        type=str,
        help="whether your processing the training or prediction data",
        required=True,
        choices=['train', 'predict']
    )
    process_parser.set_defaults(func=_run_processing)

    train_parser = subparsers.add_parser('train')

    train_parser.add_argument(
        '--raw_data_file',
        type=str,
        help="File containing the raw data",
        required=True
    )

    train_parser.add_argument(
        '--processed_data_folderpath',
        type=str,
        help="Folder containing all the processed data from the process script",
        required=True
    )

    train_parser.add_argument(
        '--model_folderpath',
        type=str,
        help="Same as the model_folderpath used in the predict script. You should store the trained model here",
        required=True
    )

    train_parser.add_argument(
        '--model_name',
        type=str,
        help="Name for the model",
        required=True
    )
    train_parser.set_defaults(func=_run_training)

    predict_parser = subparsers.add_parser('predict')

    predict_parser.add_argument(
        '--raw_data_file',
        type=str,
        help="File containing the raw data",
        required=True
    )

    predict_parser.add_argument(
        '--processed_data_folderpath',
        type=str,
        help="Folder containing all the processed data from the process script",
        required=True
    )

    predict_parser.add_argument(
        '--model_folderpath',
        type=str,
        help="Folder containing the trained models from the train script",
        required=True
    )

    predict_parser.add_argument(
        '--output_filepath',
        type=str,
        help="File that the final prediction should be saved to",
        required=True
    )

    predict_parser.add_argument(
        '--model_name',
        type=str,
        help="Name of the model",
        required=True
    )
    predict_parser.set_defaults(func=_run_prediction)

    return parser.parse_args()


# Handle direct calling of this file, you should not need to change this.
if __name__ == '__main__':
    # init logger
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    # call our main function
    main()
