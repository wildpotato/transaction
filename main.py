#!/usr/bin/python3

import argparse
import os
import pprint

from transaction import Transaction
from portfolio import Portfolio

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--record", help="record that contains your transaction history")
    parser.add_argument("-s", "--start_timestamp", help="starting time")
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-d", "--duration", type=int, help="duration after starting time")
    parser.add_argument("-v", "--verbosity_level", default=0, help="verbosity level: 0 is off")
    return parser

def main():
    p = Portfolio("record")
    p.parseRecords()
    p.calculateStockReturn()
    p.displaySummary()

if __name__ == "__main__":
    main()
