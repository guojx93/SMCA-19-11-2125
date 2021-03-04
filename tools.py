import random

def readGraph_direct(path):
    parentss = {}
    children = {}
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
        if children.get(src) is None:
            children[src] = set()
        if parentss.get(dst) is None:
            parentss[dst] = set()
        edges[(src, dst)] = 0
        children[src].add(dst)
        parentss[dst].add(src)
    for edge in edges:
        dst = edge[1]
        edges[edge] = 1 / len(parentss[dst])
    return Graph(nodes, edges, children, parentss)

def readGraph_undirect(path):
    parentss = {}
    children = {}
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
        if children.get(src) is None:
            children[src] = set()
        if children.get(dst) is None:
            children[dst] = set()
        if parentss.get(src) is None:
            parentss[src] = set()
        if parentss.get(dst) is None:
            parentss[dst] = set()
        edges[(src, dst)] = 0
        edges[(dst, src)] = 0
        children[src].add(dst)
        children[dst].add(src)
        parentss[src].add(dst)
        parentss[dst].add(src)
    for edge in edges:
        dst = edge[1]
        edges[edge] = 1 / len(parentss[dst])
    return Graph(nodes, edges, children, parentss)

class Graph:
    nodes = None
    edges = None
    children = None
    parentss = None
    def __init__(self, nodes, edges, children, parentss):
        self.nodes = nodes
        self.edges = edges
        self.children = children
        self.parentss = parentss
    def get_children(self, node):
        itsChildren = self.children.get(node)
        if itsChildren is None:
            return set()
        return self.children[node]
    def get_parentss(self, node):
        itsParentss = self.parentss.get(node)
        if itsParentss is None:
            return set()
        return self.parentss[node]

def isHappened(prob):
    if prob == 1:
        return True
    if prob == 0:
        return False
    rand = random.random()
    if rand <= prob:
        return True
    else:
        return False

def chunkIt(list, n):
    avg = len(list) / float(n)
    out = []
    last = 0.0
    while last < len(list):
        out.append(list[int(last):int(last + avg)])
        last += avg
    return out

