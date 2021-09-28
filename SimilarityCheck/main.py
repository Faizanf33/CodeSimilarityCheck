import sys
import os

from ast_graph import ASTGraph

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 ast_graph.py <subject_filename> [<filename>]")
        exit(1)

    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print("File not found: " + filename)
        exit(1)

    graph = ASTGraph(filename)
    graph.create_graph()

    print(graph)

    print("\n\n")

    other_filename = sys.argv[2]

    if not os.path.isfile(other_filename):
        print("File not found: " + other_filename)
        exit(1)

    other_graph = ASTGraph(other_filename)
    other_graph.create_graph()

    print(other_graph)

    print("\n\n")

    print("Similarity: " + str(graph.compare_graphs(other_graph)))

    # print(str(adjacency_matrix))
