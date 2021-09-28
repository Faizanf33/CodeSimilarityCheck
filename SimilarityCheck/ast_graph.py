import os
import sys
import ast
import numpy as np


class ASTGraph:
    def __init__(self, filename: str) -> None:
        self.code = filename
        self.ast_tree = ast.parse(open(filename).read())

        self.graph = {}

    def __str__(self) -> str:
        return str(self.graph)

    def create_graph(self):
        self.create_nodes()

    def create_nodes(self):
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.AST):
                new_node = str(node.__class__.__name__)

                # add node to graph
                if new_node not in self.graph:
                    self.graph[new_node] = []

                # add edges to graph
                self.create_edges(node)

    def create_edges(self, node):
        for child in ast.iter_child_nodes(node):
            new_node = str(node.__class__.__name__)

            # child node is an instance of ast.AST
            if isinstance(child, ast.AST):
                child_node = str(child.__class__.__name__)

            # child node is a string
            else:
                child_node = str(child)

            # add edge to graph
            if child_node not in self.graph[new_node]:
                self.graph[new_node].append(child_node)

            else:
                # print("Edge already exists")
                pass

    def create_adjacency_matrix(self):
        # create adjacency matrix using numpy
        adjacency_matrix = np.zeros(
            (len(self.graph), len(self.graph)), dtype=int)

        # create list of nodes
        nodes = list(self.graph.keys())
        # nodes.sort()

        # fill adjacency matrix for each node
        for i in range(len(self.graph)):
            for j in range(len(self.graph)):
                if nodes[i] in self.graph[nodes[j]]:
                    adjacency_matrix[i][j] = 1

        return adjacency_matrix

    def compare_graphs(self, other_graph):
        # create adjacency matrices
        adjacency_matrix_1 = self.create_adjacency_matrix()
        adjacency_matrix_2 = other_graph.create_adjacency_matrix()

        # compare adjacency matrices
        if np.array_equal(adjacency_matrix_1, adjacency_matrix_2):
            return True

        else:
            return False
