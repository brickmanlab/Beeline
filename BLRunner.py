#!/usr/bin/env python
# coding: utf-8

import argparse
import time

import yaml

import BLRun as br

yaml.warnings({'YAMLLoadWarning': False})


def get_parser() -> argparse.ArgumentParser:
    '''
    :return: an argparse ArgumentParser object for parsing command
        line parameters
    '''
    parser = argparse.ArgumentParser(
        description='Run pathway reconstruction pipeline.')

    parser.add_argument('--config', default='config.yaml',
        help='Path to config file')

    return parser

def parse_arguments():
    '''
    Initialize a parser and use it to parse the command line arguments
    :return: parsed dictionary of command line arguments
    '''
    parser = get_parser()
    opts = parser.parse_args()

    return opts

def main():
    opts = parse_arguments()
    config_file = opts.config


    with open(config_file, 'r') as conf:
        evaluation = br.ConfigParser.parse(conf)
    print(evaluation)
    start_time = time.process_time()
    print('Evaluation started')

    for idx in range(len(evaluation.runners)):
        evaluation.runners[idx].generateInputs()

    for idx in range(len(evaluation.runners)):
        evaluation.runners[idx].run()

    for idx in range(len(evaluation.runners)):
        evaluation.runners[idx].parseOutput()

    print('Evaluation complete')
    end_time = time.process_time()
    print(f'Execution of algorithms completed in {end_time-start_time:0.2f} seconds')


if __name__ == '__main__':
  main()
