import sys
import os

from ast_graph import ASTGraph

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ast_graph.py <filename>")
        exit(1)

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print("File not found: " + filename)
        exit(1)

    graph = ASTGraph(filename)
    graph.create_graph()

    adjacency_matrix = graph.create_adjacency_matrix()

    print(graph)
    print(str(adjacency_matrix))
