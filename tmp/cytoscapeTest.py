import json
from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from pymongo import MongoClient
import networkx as nx
import numpy as np
from numpy import pi
from qwak.GraphicalQWAK import GraphicalQWAK
from qwak.State import State
from qwak.qwak import QWAK
from qwak.Errors import StateOutOfBounds, UndefinedTimeList, EmptyProbDistList, MissingNodeInput
from dotenv import load_dotenv
import os
import random

def convert_binary_to_decimal(graph_data):
    decimal_graph = graph_data.copy()

    node_id_map = {}  # To store the mapping of original binary node IDs to decimal node IDs

    for node in decimal_graph['elements']['nodes']:
        node_id = node['data']['id']
        node_id = tuple(map(int, node_id.strip('()').split(', ')))
        decimal_id = sum(bit << i for i, bit in enumerate(reversed(node_id)))
        node['data']['id'] = str(decimal_id)
        node_id_map[node_id] = decimal_id

        node_value = node['data']['value']
        node_value = tuple(map(int, node_value))
        decimal_value = sum(bit << i for i, bit in enumerate(reversed(node_value)))
        node['data']['value'] = decimal_value

        node_name = node['data']['name']
        node_name = tuple(map(int, node_name.strip('()').split(', ')))
        decimal_name = str(sum(bit << i for i, bit in enumerate(reversed(node_name))))
        node['data']['name'] = decimal_name

    for edge in decimal_graph['elements']['edges']:
        source = edge['data']['source']
        target = edge['data']['target']
        decimal_source = node_id_map[source]
        decimal_target = node_id_map[target]
        edge['data']['source'] = decimal_source
        edge['data']['target'] = decimal_target

    return decimal_graph




n = 3
g1 = nx.cycle_graph(n)
g2 = nx.hypercube_graph(n)

print(nx.cytoscape_data(g1))
print()
print(nx.cytoscape_data(g2))
print()
print(convert_binary_to_decimal(nx.cytoscape_data(g2)))