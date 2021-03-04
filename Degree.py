import random
import copy

def readGraph(path, p):
    neighbor = {}
    edges = {}
    nodes = set()
    f = open(path, 'r')
    for line in f.readlines():
        line = line.strip()
        if not len(line) or line.startswith('#'):
            continue
        row = line.split()
        src = int(row[0])
        dst = int(row[1])
        nodes.add(src)
        nodes.add(dst)
        if neighbor.get(src) is None:
            neighbor[src] = set()
        if neighbor.get(dst) is None:
            neighbor[dst] = set()
        edges[(min(src,dst), max(src,dst))] = p
        neighbor[src].add(dst)
        neighbor[dst].add(src)
    return Graph(nodes, edges, neighbor)

class Graph:
    nodes = None
    nodes_acceptance = {}
    edges = None
    neighbor = None
    node_num = None
    edge_num = None
    def __init__(self, nodes, edges, neighbor):
        self.nodes = nodes
        self.edges = edges
        self.neighbor = neighbor
        self.node_num = len(nodes)
        self.edge_num = len(edges)
        for node in self.nodes:
            self.nodes_acceptance[node] = random.random()
    def get_neighbor(self, node):
        itsNeighbor = self.neighbor.get(node)
        if itsNeighbor is None:
            return set()
        return self.neighbor[node]

if __name__ == '__main__':
    path = "soc-wiki-Vote.txt"
    graph = readGraph(path, 0.5)
    node_degree = {}
    for node in graph.nodes:
        node_degree[node] = len(graph.get_neighbor(node))
    distribution = {}
    for node in node_degree:
        degree = node_degree[node]
        if degree not in distribution:
            distribution[degree] = 1
        else:
            distribution[degree] = distribution[degree] + 1
    print(distribution)