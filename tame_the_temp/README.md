**Note:** Make sure you add new dependencies to the requirements.txt file.

Validation/Submission Pipeline
------------
To make a submission, your code will be validated through a scoring pipeline, which will run the process, train and predict scripts to produce a final prediction which is then scored. It is recommended that you do not change the existing code structure, only add to it, to allow your code to run through this pipeline.

You are limited to 5 submissions per-day to the remote pipeline. In order to make sure your code will work when submitted, you can simulate the pipeline locally using docker containers.

In order to make a submission you must have [Docker](https://docs.docker.com/install/) installed on your machine.

**To make a submission:**
```bash
unearthed submit
```

**Note:** The containers in the remote pipeline will not have access to the internet.

Project Organization
------------

    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── prediction     <- The final resulting prediction data.
    │   ├── processed      <- Intermediate data that has been transformed.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt` (This is done during submission)
    │
    ├── scoring_function   <- The function used to score a submission. Do not modify. Modified versions
    |                         will be overwritten for remote validation.
    |
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   └── process.py <- Scripts to process data, feature selection, wrangle, etc.
    │   │                     Used for both training and prediction.
    |   |
    │   └── train.py       <- Scripts train the prediction model
    │   │
    │   └── predict.py <- Scripts to use trained models to make predictions
    |   |
    │   └── industry.py <- Scripts to load data specific to the Industry Partner's environment.


