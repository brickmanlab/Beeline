#!/usr/bin/env python

import argparse
import itertools
import pickle
from typing import Any, Dict

import pandas as pd
import yaml
from sklearn.metrics import (
    auc,
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    jaccard_score,
    matthews_corrcoef,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
    cohen_kappa_score
)


def read_config(path: str) -> Dict[str, Any]:
    with open(path) as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
        return content


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Custom GRN evaluation (TPR, FPR, F1-score)"
    )
    # arg_parser.add_argument("--folder", help="Folder path [str]", action="store", type=str)
    arg_parser.add_argument(
        "--config",
        help="Configuration file [str]",
        action="store",
        type=str,
        required=True,
    )
    args = arg_parser.parse_args()

    # config-files/Synthetic/dyn-LI.yaml
    config = read_config(args.config)
    DELIMINTER: str = "#"

    algorithms = [x["name"] for x in config["input_settings"]["algorithms"]]
    datasets = config["input_settings"]["datasets"]
    metrics = {}

    for dataset in datasets:
        metrics[dataset["name"]] = {
            alg: {
                "tn": 0,
                "fp": 0,
                "fn": 0,
                "tp": 0,
                "accuracy_score": 0,
                "brier_score_loss": 0,
                "jaccard_score": 0,
                "auroc": 0,
                "auprc": 0,
                "average_precision_score": 0,
                "f1_micro": 0,
                "f1_macro": 0,
                "f1_weighted": 0,
                "tpr": 0,
                "fpr": 0,
                "fdr": 0,
                "mcc": 0,
                "cohen_kappa": 0,
            }
            for alg in algorithms
        }

        in_path: str = (
            f"{config['input_settings']['input_dir']}/{config['input_settings']['dataset_dir']}/{dataset['name']}"
        )
        out_path: str = (
            f"{config['output_settings']['output_dir']}/{config['input_settings']['dataset_dir']}/{dataset['name']}"
        )

        for algorithm in algorithms:

            expr_file: str = f"{in_path}/{dataset['exprData']}"
            reference_file: str = f"{in_path}/{dataset['trueEdges']}"
            infered_file: str = f"{out_path}/{algorithm}/rankedEdges.csv"

            genes = pd.read_csv(expr_file, index_col=0).index

            # ignores self-edge by default
            pairwise_genes = list(
                map(DELIMINTER.join, itertools.permutations(genes, 2))
            )

            # Gold standard network
            gold_net = pd.read_csv(reference_file)
            gold_net_interactions = gold_net[["Gene1", "Gene2"]].agg(
                DELIMINTER.join, axis=1
            )

            # predicted network (rankedEdges.csv)
            predicted = pd.read_csv(infered_file, sep="\t").query("EdgeWeight > 0")
            predicted_net_interactions = predicted[["Gene1", "Gene2"]].agg(
                DELIMINTER.join, axis=1
            )
            # predicted["key"] = predicted_net_interactions

            # Dataframe containing both reference and predicted
            evaluation = pd.DataFrame(
                0, index=pairwise_genes, columns=["reference", "predicted"]
            )
            evaluation.loc[
                evaluation.index.intersection(gold_net_interactions), "reference"
            ] = 1
            evaluation.loc[
                evaluation.index.intersection(predicted_net_interactions), "predicted"
            ] = 1
            # evaluation.loc[
            #     evaluation.index.intersection(predicted_net_interactions), "predicted"
            # ] = (
            #     predicted.set_index("key")
            #     .loc[
            #         evaluation.index.intersection(predicted_net_interactions),
            #         "EdgeWeight",
            #     ]
            #     .values
            # )

            y_true, y_pred = evaluation.reference.ravel(), evaluation.predicted.ravel()

            TN, FP, FN, TP = confusion_matrix(y_true, y_pred).ravel()
            F1 = TP / (TP + 0.5 * (FP + FN))
            # TPR = TP / (TP + FN)
            # FPR = FP / (FP + TN)
            FDR = FP / (FP + TP)

            FPR, TPR, thresholds = roc_curve(y_true, y_pred, pos_label=1)
            PRECISION, RECALL, thresholds = precision_recall_curve(y_true, y_pred, pos_label=1)

            metrics[dataset["name"]][algorithm]["tn"] = TN
            metrics[dataset["name"]][algorithm]["fp"] = FP
            metrics[dataset["name"]][algorithm]["fn"] = FN
            metrics[dataset["name"]][algorithm]["tp"] = TP

            metrics[dataset["name"]][algorithm]["accuracy_score"] = accuracy_score(y_true, y_pred)
            metrics[dataset["name"]][algorithm]["brier_score_loss"] = brier_score_loss(y_true, y_pred)
            metrics[dataset["name"]][algorithm]["jaccard_score"] = jaccard_score(y_true, y_pred)
            metrics[dataset["name"]][algorithm]["auroc"] = roc_auc_score(y_true, y_pred)
            metrics[dataset["name"]][algorithm]["auprc"] = auc(RECALL, PRECISION)
            metrics[dataset["name"]][algorithm]["average_precision_score"] = average_precision_score(
                y_true, y_pred
            )
            metrics[dataset["name"]][algorithm]["f1_micro"] = f1_score(
                y_true, y_pred, average="micro"
            )
            metrics[dataset["name"]][algorithm]["f1_macro"] = f1_score(
                y_true, y_pred, average="macro"
            )
            metrics[dataset["name"]][algorithm]["f1_weighted"] = f1_score(
                y_true, y_pred, average="weighted"
            )
            metrics[dataset["name"]][algorithm]["tpr"] = TPR
            metrics[dataset["name"]][algorithm]["fpr"] = FPR
            metrics[dataset["name"]][algorithm]["fdr"] = FDR
            metrics[dataset["name"]][algorithm]["mcc"] = matthews_corrcoef(
                y_true, y_pred
            )
            metrics[dataset["name"]][algorithm]["cohen_kappa"] = cohen_kappa_score(y_true, y_pred)

    metrics_path: str = (
        f"{config['output_settings']['output_dir']}/{config['input_settings']['dataset_dir']}"
    )
    with open(f"{metrics_path}/metrics_v2.pkl", "wb") as f:
        pickle.dump(metrics, f)
