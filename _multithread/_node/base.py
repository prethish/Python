"""The goal of the module is to be able to link functions in graph
and execute them in order.
"""
import networkx as nx
import os


def find_files(_path):
    return os.listdir(_path)


def store_to_file(_content, file_path):
    with open(file_path, "w") as file_handle:
        for line in _content:
            file_handle.write(line)


G = nx.Graph()

G.add_node("find_file")
G.add_node("store_to_file")
G.add_edge("find_file", "store_to_file")

nx.draw(G)
