import tools as tools
import random
import copy

def compute(graph, seeds, R=2000):
    influence = 0
    for i in range(R):
        queue = []
        queue.extend(seeds)
        checked = copy.deepcopy(seeds)
        while len(queue) != 0:
            current_node = queue.pop(0)
            children = graph.get_children(current_node)
            for child in children:
                if child not in checked:
                    rate = graph.edges[(current_node, child)]
                    if tools.isHappened(rate):
                        checked.add(child)
                        queue.append(child)
        influence += len(checked)
    influence = influence/R
    return influence

def reverseSearch(graph, root):
    searchSet = set()
    queue = []
    queue.append(root)
    searchSet.add(root)
    while len(queue) != 0:
        current_node = queue.pop(0)
        parentss = graph.get_parentss(current_node)
        for parent in parentss:
            if parent not in searchSet:
                rate = graph.edges[(parent, current_node)]
                if tools.isHappened(rate):
                    searchSet.add(parent)
                    queue.append(parent)
    return searchSet

def generateRRset(graph):
    selectedNode = random.randint(1, len(graph.nodes))
    RRset = reverseSearch(graph, selectedNode)
    return RRset

def RRCollection(graph, theta):
    R = []
    for i in range(theta):
        RR = generateRRset(graph)
        R.append(RR)
    return R

def estimate(graph, seeds, R):
    sum = 0
    for RR in R:
        if len(seeds & RR) != 0:
            sum += 1
    influence = len(graph.nodes) * sum / len(R)
    return influence

def maxDegreeNode(graph, k):
    node_degree = {}
    for node in graph.nodes:
        node_degree[node] = len(graph.get_children(node))
    node_degree = sorted(node_degree.items(), key=lambda item: item[1], reverse=True)
    seeds = set()
    for i in range(k):
        if i % 2 == 0:
            node = node_degree[i][0]
            seeds.add(node)
    return seeds

if __name__ == '__main__':
    path = "soc-sign-bitcoinalpha.txt"
    graph = tools.readGraph_direct(path)
    seeds = maxDegreeNode(graph, 40)
    print(seeds)
    # influence = compute(graph, seeds)
    # print(influence)
    # R = RRCollection(graph, 20000)
    # influence = estimate(graph, seeds, R)
    # print(influence)

    # f = open("./soc-sign-bitcoinalpha-value", 'w+')
    # for node in graph.nodes:
    #     benefit = random.uniform(0,1)
    #     influencedbenefit = random.uniform(-1, benefit)
    #     print(str(node) + " " + str(benefit) + " " + str(influencedbenefit), file=f)