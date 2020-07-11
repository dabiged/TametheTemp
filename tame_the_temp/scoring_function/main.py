import argparse
from scoring_function import score
import logging

def main():
    args = _parse_args()
    args.func(args)

def _parse_args():
    scoring_parser = argparse.ArgumentParser('Predict')

    scoring_parser.add_argument(
        '--prediction_filepath',
        type=str,
        required=True
    )

    scoring_parser.add_argument(
        '--public_actual_filepath',
        type=str,
        required=True
    )

    scoring_parser.add_argument(
        '--private_actual_filepath',
        type=str,
        required=True
    )

    scoring_parser.add_argument(
        '--score_filepath',
        type=str,
        required=True
    )
    scoring_parser.set_defaults(func=_run_scoring)

    return scoring_parser.parse_args()

def _run_scoring(args):
    score(args.prediction_filepath, args.public_actual_filepath, args.private_actual_filepath, args.score_filepath)

# Handle direct calling of this file, you should not need to change this.
if __name__ == '__main__':
    # init logger
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    # call our main function
    main()
