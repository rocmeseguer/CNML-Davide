#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import sys
import random

from igraph import *

from fileReader import cnmlReader
from graphAnalysis import getLargestComponent, getCoreGraph, computeRobustness

def main(argv):
	network = sys.argv[1]

	graph = cnmlReader(sys.argv[2])
	base = getLargestComponent(graph)
	core = getCoreGraph(base.copy())

	df = pd.DataFrame(data = {
		"network" : [],
		"method" : [],
		"robustness" : []
	})

	for i in range(100):
		df = df.append({
			'network': network,
			'method': 'random',
			'robustness': computeRobustness(core, "random")
			},
			ignore_index=True)

	df = df.append({
		'network': network,
		'method': 'degree',
		'robustness': computeRobustness(core, "degree")
		},
		ignore_index=True)

	df = df.append({
		'network': network,
		'method': 'betweenness',
		'robustness': computeRobustness(core, "betweenness")
		},
		ignore_index=True)

	df = df.append({
		'network': network,
		'method': 'closeness',
		'robustness': computeRobustness(core, "closeness")
		},
		ignore_index=True)

	df.to_csv("./" + str(network) + "_r.csv")

if __name__ == '__main__':
		main(sys.argv)
