#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import operator
import random

from igraph import *

def getLargestComponent(graph):
    return(graph.components().giant())


def getCoreGraph(graph):
	vs = graph.vs(_degree=1)
	graph.delete_vertices(vs)

	return(graph)

def getTopDegreeCandidate(graph):
    cls_dict = dict([(idx, cls) for idx, cls in enumerate(graph.degree())])
    sorted_cls = sorted(cls_dict.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_cls[0][0]


def getTopBetweennessCandidate(graph):
	cls_dict = dict([(idx, cls) for idx, cls in enumerate(graph.betweenness())])
	sorted_cls = sorted(cls_dict.items(), key=operator.itemgetter(1), reverse=True)

	return sorted_cls[0][0]


def getTopClosenessCandidate(graph):
	cls_dict = dict([(idx, cls) for idx, cls in enumerate(graph.closeness())])
	sorted_cls = sorted(cls_dict.items(), key=operator.itemgetter(1), reverse=True)

	return sorted_cls[0][0]

def computeRobustness(graph, method):
    gr = graph.copy()

    N = gr.vcount()

    count_sum = N
    i = 1
    while gr.vcount() > 1:
        if method == 'degree':
            candidate = getTopDegreeCandidate(gr)

        elif method == 'betweenness':
            candidate = getTopBetweennessCandidate(gr)

        elif method == 'closeness':
            candidate = getTopClosenessCandidate(gr)

        else:
            candidate = random.choice(gr.vs)

        gr.delete_vertices(candidate)
        gr = getLargestComponent(gr)

        count_sum = count_sum + gr.vcount()
        i = i + 1

    A2 = N * N
    A1 = (2 * count_sum) - N
    return(A1 / A2)
