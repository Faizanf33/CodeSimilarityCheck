import ast
import sys
import os
import pydot
import astor
import subprocess


class ASTVisalize:
    def __init__(self, filename: str):
        self.code = filename
        self.ast = ast.parse(self.code)
        self.astor = astor.code_gen.to_source(self.ast)

        # self.ast = ast.parse(self.code)
        self.graph = pydot.Dot(graph_type='digraph')
        # self.graph.set_node_defaults(shape='box')
        # self.graph.set_edge_defaults(arrowhead='open')
        # self.graph.set_graph_defaults(rankdir='LR')
        # self.graph.set_node_defaults(fontsize='12')
        # self.graph.set_edge_defaults(fontsize='12')
        # self.graph.set_graph_defaults(fontsize='12')
        # self.graph.set_node_defaults(fontcolor='black')
        # self.graph.set_edge_defaults(fontcolor='teal')
        # self.graph.set_graph_defaults(fontcolor='black')

    def get_astor(self):
        return self.astor

    def create_graph(self):
        self.create_nodes()
        return self.graph

    def create_simplified_graph(self):
        self.create_nodes()
        self.graph.set_simplify(True)
        return self.graph

    def create_nodes(self):
        for node in ast.walk(self.ast):
            if isinstance(node, ast.AST):
                new_node = pydot.Node(str(node.__class__.__name__))
                new_node.set_shape('box')
                self.graph.add_node(new_node)

                self.create_edges(node)

    def create_edges(self, node: ast.AST):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.AST):
                edge = pydot.Edge(str(node.__class__.__name__),
                                  str(child.__class__.__name__))

                self.graph.add_edge(edge)   # add edge to graph

            else:
                edge = pydot.Edge(str(node.__class__.__name__),
                                  str(child))

                self.graph.add_edge(edge)   # add edge to graph

    def get_graph(self):
        return self.graph

    def compare_graphs(self, other_graph):
        # return self.graph.compare(other_graph)
        ...  # remove these dots to complete function definition

    def save_dot(self, filename: str):
        self.graph.write_dot(filename)

    def save_graph(self, filename: str):
        self.graph.write_png(filename)

    def show_graph(self, filename: str):
        self.graph.write_png(filename)

        if os.name == 'nt':
            os.startfile(filename)

        else:
            opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
            subprocess.call([opener, filename])

    def get_code(self):
        return self.code

    def get_ast(self):
        return self.ast


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 ast_visualize.py <filename> [<filename> ...]')
        sys.exit(1)

    filename = sys.argv[1]

    file = open(filename, 'r')
    output = sys.argv[2]

    ast_graph = ASTVisalize(file.read())

    # ast_graph.create_graph()
    # ast_graph.save_graph('ast_graph.png')

    ast_graph.create_simplified_graph()
    # ast_graph.save_dot('ast_graph.dot')

    # ast_graph.save_dot('ast_graph_simplified.dot')
    # ast_graph.save_graph('ast_graph_simplified.png')

    ast_graph.show_graph(output)
    # print(ast_graph.get_code())
    # print(ast_graph.get_graph())

    file.close()
