# prozhitoML
Analysis using machine learning metrics to study change over time in a corpus of diaries 

## Install dependencies from requirements file 
- `pip install -r requirements.txt`

## Convert the Django json dump to jsonl data, create test and train split.
-  `python -m spacy project run  load_json ./ru_time_metrics_model`

## Convert jsonl to spaCy binary format 
-  `python -m spacy project run convert ./ru_time_metrics_model`

## Train a single model using spaCy default parameters
-  `python -m spacy project run train ./ru_time_metrics_model`

## To run sweeps for hyperparameter search and logging using Weights and Biases 

- ` wandb sweep ./ru_time_metrics_model/scripts/sweep.yml`
- `wandb agent apjanco/prozhitoML/pultt969` (use id printed in "Run sweep agent with")