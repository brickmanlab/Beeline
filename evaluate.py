#!/usr/bin/env python

import argparse
import subprocess
import glob
import yaml
import pandas as pd
import itertools
import numpy as np
from typing import Any, Dict
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, roc_auc_score, roc_curve, precision_recall_curve, auc, confusion_matrix, adjusted_rand_score
from sklearn.preprocessing import MinMaxScaler
from rpy2.robjects.packages import importr
from rpy2.robjects import FloatVector


def read_config(path: str) -> Dict[str, Any]:
    with open(path) as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
        return content


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(
        description="Custom GRN evaluation (TPR, FPR, F1-score)"
    )
    # arg_parser.add_argument("--folder", help="Folder path [str]", action="store", type=str)
    arg_parser.add_argument("--config", help="Configuration file [str]", action="store", type=str, required=True)
    args = arg_parser.parse_args()

    # config-files/Synthetic/dyn-LI.yaml
    config = read_config(args.config)
    joiner: str = "#"

    algorithms = [x['name'] for x in config['input_settings']['algorithms']]

    metrics_auroc = []
    metrics_tpr = []
    metrics_fpr = []
    metrics_f1 = []
    metrics_ri = []
    for dataset in config['input_settings']['datasets']:

        aurocs, tprs, fprs, f1s, ris = [], [], [], [], []

        in_path: str = f"{config['input_settings']['input_dir']}/{config['input_settings']['dataset_dir']}/{dataset['name']}"
        out_path: str = f"{config['output_settings']['output_dir']}/{config['input_settings']['dataset_dir']}/{dataset['name']}"
        
        for algorithm in algorithms:

            expr_file: str = f"{in_path}/{dataset['exprData']}"
            reference_file: str = f"{in_path}/{dataset['trueEdges']}"
            infered_file: str = f"{out_path}/{algorithm}/rankedEdges.csv"

            genes = pd.read_csv(expr_file, index_col=0).index
            
            # ignores self-edge by default
            permutations = [f"{x[0]}{joiner}{x[1]}" for x in itertools.permutations(genes, 2)]

            df = pd.DataFrame(0, index=permutations, columns=['reference', 'predicted'])

            # create labels from reference.csv
            reference = pd.read_csv(reference_file)
            reference = [f"{x[0]}{joiner}{x[1]}" for x in zip(reference['Gene1'], reference['Gene2']) if x[0] != x[1]]
            df.loc[reference, 'reference'] = 1.0

            # create prediction from rankedEdges.csv
            infered_df = pd.read_csv(infered_file, sep='\t')
            infered_df['pairwise'] = infered_df[['Gene1', 'Gene2']].agg(f'{joiner}'.join, axis=1)
            infered_df = infered_df.set_index('pairwise')

            # get common gene pairwise
            common_pairwise = np.intersect1d(infered_df.index, df.index)
            df.loc[common_pairwise, 'predicted'] = infered_df.loc[common_pairwise, 'EdgeWeight'].values

            fpr, tpr, thresholds = roc_curve(y_true=df['reference'],
                                            y_score=df['predicted'], pos_label=1)

            # prec, recall, thresholds = precision_recall_curve(y_true=df['reference'],
            #                                                 probas_pred=df['predicted'], pos_label=1)

            y_true = df['reference'].values
            predicted = df['predicted'].values.astype(np.float32)
            y_pred = np.round(np.interp(predicted, (predicted.min(), predicted.max()), (0, 1)))
            # y_pred = np.round(np.interp(df['predicted'].values, (df['predicted'].values.min(), df['predicted'].values.max()), (0, 1)))
            TN, FP, FN, TP = confusion_matrix(y_true, y_pred).ravel()
            F1 = TP / (TP + 0.5 * (FP + FN))
            TPR = TP / (TP + FN)
            FPR = FP / (FP + TN)
            AUROC = auc(fpr, tpr)
            # RI = adjusted_rand_score(y_true, y_pred)
            RI = (TP + TN) / (TP + FP + FN + TN)

            aurocs.append(AUROC)
            tprs.append(TPR)
            fprs.append(FPR)
            f1s.append(F1)
            ris.append(RI)

        metrics_auroc.append([dataset['name']] + aurocs)
        metrics_tpr.append([dataset['name']] + tprs)
        metrics_fpr.append([dataset['name']] + fprs)
        metrics_f1.append([dataset['name']] + f1s)
        metrics_ri.append([dataset['name']] + ris)
    
    metrics_path: str = f"{config['output_settings']['output_dir']}/{config['input_settings']['dataset_dir']}"

    pd.DataFrame(metrics_auroc, columns=['dataset'] + algorithms).set_index('dataset').to_csv(f"{metrics_path}/auroc.csv")
    pd.DataFrame(metrics_tpr, columns=['dataset'] + algorithms).set_index('dataset').to_csv(f"{metrics_path}/tpr.csv")
    pd.DataFrame(metrics_fpr, columns=['dataset'] + algorithms).set_index('dataset').to_csv(f"{metrics_path}/fpr.csv")
    pd.DataFrame(metrics_f1, columns=['dataset'] + algorithms).set_index('dataset').to_csv(f"{metrics_path}/f1.csv")
    pd.DataFrame(metrics_ri, columns=['dataset'] + algorithms).set_index('dataset').to_csv(f"{metrics_path}/ri.csv")
