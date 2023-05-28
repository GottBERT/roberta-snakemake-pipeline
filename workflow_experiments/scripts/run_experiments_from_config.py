#!/usr/bin/env python3

from pathlib import Path
from farm.experiment import (
    run_experiment,
    load_experiments,
)
import os

rundir = os.path.dirname(os.path.abspath(__file__))

config_files = [
    Path(f"{rundir}/experiments/ner/conll2003_de_config.json"),
    Path(f"{rundir}/experiments/ner/germEval14_config.json"),
    Path(f"{rundir}/experiments/text_classification/germEval18Fine_config.json"),
    Path(f"{rundir}/experiments/text_classification/germEval18Coarse_config.json"),
    Path(f"{rundir}/experiments/text_classification/gnad_config.json"),
]

for conf_file in config_files:
    experiments = load_experiments(conf_file)
    for experiment in experiments:
        run_experiment(experiment)
