#!/bin/bash

set -e

cd Algorithms/CCM/ && docker build . -t ccm:base && cd .. && cd ..

# run networks
python BLRunner.py --config config-files/config.yaml

# evaluate
python evaluate.py --config config-files/config.yaml
