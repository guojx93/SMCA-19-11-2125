import tools as tools
import IM
import copy
import numpy as np
import time

def compute(graph, S_r, benefits, influencedbenefits, S_p, R=2000):
    OverallBenefit = 0
    for i in range(R):
        queue = []
        queue.extend(S_p)
        PInfNodes = copy.deepcopy(S_p)
        while len(queue) != 0:
            current_node = queue.pop(0)
            children = graph.get_children(current_node)
            for child in children:
                if child not in PInfNodes:
                    rate = graph.edges[(current_node, child)]
                    if tools.isHappened(rate):
                        PInfNodes.add(child)
                        queue.append(child)
        queue = []
        queue.extend(S_r)
        RInfNodes = copy.deepcopy(S_r)
        while len(queue) != 0:
            current_node = queue.pop(0)
            children = graph.get_children(current_node)
            for child in children:
                if child not in RInfNodes:
                    rate = graph.edges[(current_node, child)]
                    if tools.isHappened(rate):
                        RInfNodes.add(child)
                        queue.append(child)
        for node in PInfNodes:
            # OverallBenefit += benefits[node]
            if node in RInfNodes:
                OverallBenefit += influencedbenefits[node]
            else:
                OverallBenefit += benefits[node]
    OverallBenefit = OverallBenefit/R
    return OverallBenefit

def getBenefit(path):
    f = open(path, 'r')
    benefits = {}
    influencedbenefits = {}
    for line in f.readlines():
        line = line.strip()
        row = line.split()
        node = int(row[0])
        benefits[node] = float(row[1])
        influencedbenefits[node] = float(row[2])
    return benefits, influencedbenefits

def generateWDist(graph, benefits):
    nodeList = []
    nodeDist = []
    P = 0
    for node in graph.nodes:
        P += benefits[node]
    for node in graph.nodes:
        nodeList.append(node)
        nodeDist.append(benefits[node] / P)
    nodeDist = np.array(nodeDist)
    return P, nodeList, nodeDist

def generateRW(graph, nodeList, nodeDist):
    selectedNode = np.random.choice(nodeList, p=nodeDist.ravel())
    RRSet = IM.reverseSearch(graph, selectedNode)
    return RRSet

def RWCollection(graph, theta, benefits):
    P, nodeList, nodeDist = generateWDist(graph, benefits)
    R = []
    for i in range(theta):
        RRSet = generateRW(graph, nodeList, nodeDist)
        R.append(RRSet)
    return R

def generateZDist(graph, benefits, influencedbenefits):
    nodeList = []
    nodeDist = []
    Q = 0
    for node in graph.nodes:
        Q += benefits[node] - influencedbenefits[node]
    for node in graph.nodes:
        nodeList.append(node)
        nodeDist.append((benefits[node] - influencedbenefits[node]) / Q)
    nodeDist = np.array(nodeDist)
    return Q, nodeList, nodeDist

def generateRZ(graph, nodeList, nodeDist):
    selectedNode = np.random.choice(nodeList, p=nodeDist.ravel())
    RRSet1 = IM.reverseSearch(graph, selectedNode)
    RRSet2 = IM.reverseSearch(graph, selectedNode)
    return (RRSet1, RRSet2)

def RZCollection(graph, theta, benefits, influencedbenefits):
    Q, nodeList, nodeDist = generateZDist(graph, benefits, influencedbenefits)
    R = []
    for i in range(theta):
        RRSet = generateRZ(graph, nodeList, nodeDist)
        R.append(RRSet)
    return R

def estimateW(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz):
    P, nodeList, nodeDist = generateWDist(graph, benefits)
    sum = 0
    for RRSet in Rw:
        if not S_p.isdisjoint(RRSet):
            sum += 1
    w = P * sum / len(Rw)
    return w

def estimateZ(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz):
    Q, nodeList, nodeDist = generateZDist(graph, benefits, influencedbenefits)
    sum = 0
    for RRSet in Rz:
        if not S_p.isdisjoint(RRSet[0]) and not S_r.isdisjoint(RRSet[1]):
            sum += 1
    z = Q * sum / len(Rz)
    return z

def getbenefit(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz):
    return estimateW(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz) - estimateZ(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz)

if __name__ == '__main__':
    path = "soc-wiki-Vote.txt"
    graph = tools.readGraph_direct(path)
    benefits, influencedbenefits = getBenefit("soc-wiki-Vote-value")
    S_r = {769, 399, 273, 536, 538, 416, 550, 807, 170, 560}
    S_p = {697, 317, 709, 458, 471, 351, 738, 617, 496, 123}
    overallBenefit = compute(graph, S_r, benefits, influencedbenefits, S_p)
    print(overallBenefit)
    theta = 10000
    Rw = RWCollection(graph, theta, benefits)
    Rz = RZCollection(graph, theta, benefits, influencedbenefits)
    time_start = time.time()
    overallBenefit = getbenefit(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz)
    time_end = time.time()
    print(overallBenefit)
    print(time_end - time_start)