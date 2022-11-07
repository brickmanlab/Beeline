#!/bin/bash

set -e

# rm -rf outputs/Synthetic/dyn-*/*.csv
# rm -rf inputs/Synthetic/*/*/CCM
# rm -rf outputs/Synthetic/*/*/CCM

# cd Algorithms/CCM/ && docker build . -t ccm:base && cd .. && cd ..

# run networks
#python BLRunner.py --config config-files/Synthetic/dyn-BF.yaml
#python BLRunner.py --config config-files/Synthetic/dyn-BFC.yaml
#python BLRunner.py --config config-files/Synthetic/dyn-CY.yaml
python BLRunner.py --config config-files/Synthetic/dyn-LI.yaml
python BLRunner.py --config config-files/Synthetic/dyn-LL.yaml
#python BLRunner.py --config config-files/Synthetic/dyn-TF.yaml

# evaluation
#python BLEvaluator.py --config config-files/Synthetic/dyn-BF.yaml --auc
#python BLEvaluator.py --config config-files/Synthetic/dyn-BFC.yaml --auc
#python BLEvaluator.py --config config-files/Synthetic/dyn-CY.yaml --auc
python BLEvaluator.py --config config-files/Synthetic/dyn-LI.yaml --auc
python BLEvaluator.py --config config-files/Synthetic/dyn-LL.yaml --auc
#python BLEvaluator.py --config config-files/Synthetic/dyn-TF.yaml --auc

#python evaluate.py --config config-files/Synthetic/dyn-BF.yaml
#python evaluate.py --config config-files/Synthetic/dyn-BFC.yaml
#python evaluate.py --config config-files/Synthetic/dyn-CY.yaml
python evaluate.py --config config-files/Synthetic/dyn-LI.yaml
python evaluate.py --config config-files/Synthetic/dyn-LL.yaml
#python evaluate.py --config config-files/Synthetic/dyn-TF.yaml
