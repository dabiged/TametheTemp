.PHONY: data requirements

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = nc_autoclave
MODEL_NAME = $(PROJECT_NAME)
PYTHON_INTERPRETER = python3
DOCKER_IMAGE = qc5i1je5hh.execute-api.us-east-2.amazonaws.com/unearthed/crowd-ml-nc_autoclave:latest
DOCKER_DIR = /home/jovyan

#################################################################################
# COMMANDS                                                                      #
#################################################################################

docker_run:
	docker run --rm -v "$(PROJECT_DIR):$(DOCKER_DIR)" ${DOCKER_IMAGE} bash -c '$(cmd)'

## Install Python Dependencies
requirements:
	cat requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel python-dotenv click Sphinx coverage flake8
	# Ensure requirements.txt exists.
	cat requirements.txt
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Train Model
train:
	mkdir -p dist/processed
	$(PYTHON_INTERPRETER) main.py train --raw_data_file data/raw/train/20190601162260 --processed_data_folderpath data/processed --model_folderpath models --model_name $(MODEL_NAME)

## This is how the predictions are made for the competition
predict:
	mkdir -p dist/processed
	mkdir -p data/prediction
	$(PYTHON_INTERPRETER) main.py predict --raw_data_file data/raw/test/20190601162260 --processed_data_folderpath data/processed --model_folderpath models --output_filepath ./data/prediction/prediction.csv --model_name $(MODEL_NAME)

## This is how the score will be calculated in the competition
score:
	$(PYTHON_INTERPRETER) scoring_function/main.py \
		--prediction_filepath data/prediction/prediction.csv \
		--public_actual_filepath data/secret/publicLeaderboard_target.csv \
        --private_actual_filepath data/secret/privateLeaderboard_target.csv \
        --score_filepath data/prediction/score.txt

## Run Pipeline
pipeline:
	make train
	make predict
	make score

## Build into package
build:requirements
	rm -rf dist build *.egg-info
	$(PYTHON_INTERPRETER) setup.py sdist bdist_wheel
	cp dist/*.tar.gz dist/src.tar.gz

# Freeze deps
freeze:
	pip freeze > requirements.txt

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
