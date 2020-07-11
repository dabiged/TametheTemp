#!/bin/bash
cd tame_the_temp
python main.py train \
	--raw_data_file='data/raw/train/20190601162260/' \
	--processed_data_folderpath='data/processed/' \
	--model_folderpath='models/' \
	--model_name="basic-lags" && \
python main.py predict \
	--raw_data_file='data/raw/train/20190601162260/' \
	--processed_data_folderpath='data/processed/' \
	--model_folderpath='models/' \
	--model_name="basic-lags" \
	--output_filepath='output/basic_lags'
