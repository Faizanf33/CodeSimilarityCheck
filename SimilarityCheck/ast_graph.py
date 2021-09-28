import os
import sys
import ast


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
        ...
        # create adjacency matrix
        # matrix = []

        # # create rows
        # for i in range(len(self.graph)):
        #     matrix.append([])

        #     # create columns
        #     for j in range(len(self.graph)):
        #         matrix[i].append(0)

        # # set adjacency matrix
        # for key, value in self.graph.items():
        #     key_index = self.ma.keys().index(key)

        #     for item in value:
        #         item_index = self.graph.values().index(item)

        #         # set edge weight
        #         matrix[key_index][item_index] = 1

        # return matrix

        # self.adjacency_matrix = {}

        # for node in self.graph:
        #     self.adjacency_matrix[node] = []

        #     for child in self.graph[node]:
        #         self.adjacency_matrix[node].append(child)

        # return self.adjacency_matrix
