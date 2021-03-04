import tools as tools
import IM
import copy
import numpy as np
import objectiveEstimation as oe
import random
import math
import time

def greedy(graph, S_r, k, benefits, influencedbenefits, Rw, Rz):
    time_start = time.time()
    S_p = set()
    overallBenefit = 0
    for i in range(1, k + 1):
        candidate = graph.nodes - S_p
        max_node = float("-inf")
        max_gain = float("-inf")
        for node in candidate:
            S_pPrime = copy.deepcopy(S_p)
            S_pPrime.add(node)
            currentGain = oe.getbenefit(graph, S_pPrime, S_r, benefits, influencedbenefits, Rw, Rz) - overallBenefit
            if currentGain > max_gain:
                max_node = node
                max_gain = currentGain
        if max_gain < 0:
            break
        S_p.add(max_node)
        overallBenefit += max_gain
        if i % 5 == 0:
            time_end = time.time()
            print("k: " + str(i) + " overallBenefit: " + str(overallBenefit) + " time: " + str(time_end - time_start))
    return S_p, overallBenefit

def upperbound_1(graph, X, Y, S_r, func, benefits, influencedbenefits, Rw, Rz):
    first = func(graph, X, S_r, benefits, influencedbenefits, Rw, Rz)
    second = 0
    for j in X - Y:
        second += first - func(graph, X - {j}, S_r, benefits, influencedbenefits, Rw, Rz)
    third = 0
    for j in Y - X:
        third += func(graph, {j}, S_r, benefits, influencedbenefits, Rw, Rz)
    return first - second + third

def upperbound_2(graph, X, Y, S_r, func, benefits, influencedbenefits, Rw, Rz):
    first = func(graph, X, S_r, benefits, influencedbenefits, Rw, Rz)
    second = 0
    total = func(graph, graph.nodes, S_r, benefits, influencedbenefits, Rw, Rz)
    for j in X - Y:
        second += total - func(graph, graph.nodes - {j}, S_r, benefits, influencedbenefits, Rw, Rz)
    third = 0
    for j in Y - X:
        third += func(graph, X | {j}, S_r, benefits, influencedbenefits, Rw, Rz) - first
    return first - second + third

def selectAlpha1(graph, X):
    XList = list(X)
    random.shuffle(XList)
    XDList = list(graph.nodes - X)
    random.shuffle(XDList)
    alpha = XList + XDList
    return alpha

def selectAlpha2(graph, X):
    UnitValue = {}
    for node in graph.nodes:
        UnitValue[node] = oe.getbenefit(graph, {node}, S_r, benefits, influencedbenefits, Rw, Rz)
    UnitValue = sorted(UnitValue.items(), key=lambda item: item[1], reverse=True)
    XList = []
    XDList = []
    for i in range(len(graph.nodes)):
        if UnitValue[i][0] in X:
            XList.append(UnitValue[i][0])
        else:
            XDList.append(UnitValue[i][0])
    alpha = XList + XDList
    return alpha

def selectAlpha3(graph, X):
    UnitValue = {}
    for node in graph.nodes:
        UnitValue[node] = oe.estimateW(graph, {node}, S_r, benefits, influencedbenefits, Rw, Rz)
    UnitValue = sorted(UnitValue.items(), key=lambda item: item[1], reverse=True)
    XList = []
    XDList = []
    for i in range(len(graph.nodes)):
        if UnitValue[i][0] in X:
            XList.append(UnitValue[i][0])
        else:
            XDList.append(UnitValue[i][0])
    alpha = XList + XDList
    return alpha

def selectAlpha4(graph, X):
    UnitValue = {}
    for node in graph.nodes:
        UnitValue[node] = oe.estimateZ(graph, {node}, S_r, benefits, influencedbenefits, Rw, Rz)
    UnitValue = sorted(UnitValue.items(), key=lambda item: item[1], reverse=False)
    XList = []
    XDList = []
    for i in range(len(graph.nodes)):
        if UnitValue[i][0] in X:
            XList.append(UnitValue[i][0])
        else:
            XDList.append(UnitValue[i][0])
    alpha = XList + XDList
    return alpha

def lowerbound(graph, Y, S_r, alpha, func, benefits, influencedbenefits, Rw, Rz):
    lowerValue = 0
    for node in Y:
        i = alpha.index(node)
        lowerValue += func(graph, set(alpha[0:i+1]), S_r, benefits, influencedbenefits, Rw, Rz) \
                    - func(graph, set(alpha[0:i]), S_r, benefits, influencedbenefits, Rw, Rz)
    return lowerValue

def modular_modular(graph, func, ubound, S_r, k, benefits, influencedbenefits, Rw, Rz):
    S_p = set()
    while True:
        alpha = func(graph, S_p)
        UnitValue = {}
        zero = (lowerbound(graph, set(), S_r, alpha, oe.estimateW, benefits, influencedbenefits, Rw, Rz) \
             - ubound(graph, S_p, set(), S_r, oe.estimateZ, benefits, influencedbenefits, Rw, Rz))
        for node in graph.nodes:
            UnitValue[node] = (lowerbound(graph, {node}, S_r, alpha, oe.estimateW, benefits, influencedbenefits, Rw, Rz) \
                            - ubound(graph, S_p, {node}, S_r, oe.estimateZ, benefits, influencedbenefits, Rw, Rz)) \
                            - zero
        NewS_p = set()
        for i in range(k):
            max_node = max(UnitValue, key=UnitValue.get)
            if UnitValue[max_node] < 0:
                break
            NewS_p.add(max_node)
            del UnitValue[max_node]
        if NewS_p == S_p:
            break
        S_p = NewS_p
        # print(S_p)
        print(oe.getbenefit(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz))
    overallBenefit = oe.getbenefit(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz)
    return S_p, overallBenefit

def pi(graph, func, ubound, X, S_r, k, benefits, influencedbenefits, Rw, Rz):
    alpha = func(graph, X)
    UnitValue = {}
    zero = ubound(graph, X, set(), S_r, oe.estimateW, benefits, influencedbenefits, Rw, Rz) \
         - lowerbound(graph, set(), S_r, alpha, oe.estimateZ, benefits, influencedbenefits, Rw, Rz)
    for node in graph.nodes:
        UnitValue[node] = ubound(graph, X, {node}, S_r, oe.estimateW, benefits, influencedbenefits, Rw, Rz) \
                        - lowerbound(graph, {node}, S_r, alpha, oe.estimateZ, benefits, influencedbenefits, Rw, Rz) \
                        - zero
    seeds = set()
    for i in range(k):
        max_node = max(UnitValue, key=UnitValue.get)
        if UnitValue[max_node] < 0:
            break
        seeds.add(max_node)
        del UnitValue[max_node]
    UB = ubound(graph, X, seeds, S_r, oe.estimateW, benefits, influencedbenefits, Rw, Rz) \
       - lowerbound(graph, seeds, S_r, alpha, oe.estimateZ, benefits, influencedbenefits, Rw, Rz)
    return seeds, UB

def approximation(graph, func, X, S_r, k, benefits, influencedbenefits, Rw, Rz, delta):
    P, nodeList, nodeDist = oe.generateWDist(graph, benefits)
    Q, nodeList, nodeDist = oe.generateZDist(graph, benefits, influencedbenefits)
    seeds, UB1 = pi(graph, func, upperbound_1, X, S_r, k, benefits, influencedbenefits, Rw, Rz)
    seeds, UB2 = pi(graph, func, upperbound_2, X, S_r, k, benefits, influencedbenefits, Rw, Rz)
    UBB1 = UB1 + (P + Q) * math.sqrt(1 / (2 * theta) * math.log(4 / delta))
    UBB2 = UB2 + (P + Q) * math.sqrt(1 / (2 * theta) * math.log(4 / delta))
    OB = oe.getbenefit(graph, X, S_r, benefits, influencedbenefits, Rw, Rz)
    return max(OB/UBB1, OB/ UBB2)

def randomm(graph, S_r, k, benefits, influencedbenefits, Rw, Rz):
    S_p = set()
    for i in range(k):
        candidate = list(graph.nodes)
        nindex = random.randint(0, len(candidate) - 1)
        node = candidate[nindex]
        S_p.add(node)
        del candidate[nindex]
        if (i + 1) % 5 == 0:
            overallBenefit = oe.getbenefit(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz)
            print("k: " + str(i+1) + " overallBenefit: " + str(overallBenefit))
    overallBenefit = oe.getbenefit(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz)
    return S_p, overallBenefit

def maxDegree(graph, S_r, k, benefits, influencedbenefits, Rw, Rz):
    node_degree = {}
    for node in graph.nodes:
        node_degree[node] = len(graph.get_children(node))
    node_degree = sorted(node_degree.items(), key=lambda item: item[1], reverse=True)
    S_p = set()
    for i in range(k):
        node = node_degree[i][0]
        S_p.add(node)
        if (i + 1) % 5 == 0:
            overallBenefit = oe.getbenefit(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz)
            print("k: " + str(i+1) + " overallBenefit: " + str(overallBenefit))
    overallBenefit = oe.getbenefit(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz)
    return S_p, overallBenefit

def maxInf(graph, S_r, k, benefits, influencedbenefits, Rw, Rz):
    time_start = time.time()
    S_p = set()
    Benefit = 0
    for i in range(1, k + 1):
        candidate = graph.nodes - S_p
        max_node = float("-inf")
        max_gain = float("-inf")
        for node in candidate:
            S_pPrime = copy.deepcopy(S_p)
            S_pPrime.add(node)
            currentGain = oe.estimateW(graph, S_pPrime, S_r, benefits, influencedbenefits, Rw, Rz) - Benefit
            if currentGain > max_gain:
                max_node = node
                max_gain = currentGain
        if max_gain < 0:
            break
        S_p.add(max_node)
        Benefit += max_gain
        if i % 5 == 0:
            time_end = time.time()
            overallBenefit = oe.getbenefit(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz)
            print("k: " + str(i) + " overallBenefit: " + str(overallBenefit) + " time: " + str(time_end - time_start))
    overallBenefit = oe.getbenefit(graph, S_p, S_r, benefits, influencedbenefits, Rw, Rz)
    return S_p, overallBenefit

if __name__ == '__main__':
    path = "soc-wiki-Vote.txt"
    graph = tools.readGraph_direct(path)
    benefits, influencedbenefits = oe.getBenefit("soc-wiki-Vote-value")
    # S_r = {1, 4, 13, 21, 26, 30, 32, 33, 169, 170, 45, 303, 67, 69, 86, 95, 100, 231, 113, 119}
    S_r = {769, 399, 273, 536, 538, 416, 550, 807, 170, 560, 697, 317, 709, 458, 471, 351, 738, 617, 496, 123}
    # S_r = {2, 9, 529, 660, 277, 541, 682, 50, 691, 563, 565, 71, 712, 585, 80, 350, 611, 613, 744, 877}

    theta = 2000
    print("theta = " + str(theta))
    Rw = oe.RWCollection(graph, theta, benefits)
    Rz = oe.RZCollection(graph, theta, benefits, influencedbenefits)

    # k = 20
    # print("upperbound_1")
    # S_p, overallBenefit = modular_modular(graph, selectAlpha1, upperbound_1, S_r, k, benefits, influencedbenefits, Rw, Rz)
    # print("objective: " + str(overallBenefit))
    # S_p, overallBenefit = modular_modular(graph, selectAlpha2, upperbound_1, S_r, k, benefits, influencedbenefits, Rw, Rz)
    # print("objective: " + str(overallBenefit))
    # S_p, overallBenefit = modular_modular(graph, selectAlpha3, upperbound_1, S_r, k, benefits, influencedbenefits, Rw, Rz)
    # print("objective: " + str(overallBenefit))
    # S_p, overallBenefit = modular_modular(graph, selectAlpha4, upperbound_1, S_r, k, benefits, influencedbenefits, Rw, Rz)
    # print("objective: " + str(overallBenefit))
    #
    # print("upperbound_2")
    # S_p, overallBenefit = modular_modular(graph, selectAlpha1, upperbound_2, S_r, k, benefits, influencedbenefits, Rw, Rz)
    # print("objective: " + str(overallBenefit))
    # S_p, overallBenefit = modular_modular(graph, selectAlpha2, upperbound_2, S_r, k, benefits, influencedbenefits, Rw, Rz)
    # print("objective: " + str(overallBenefit))
    # S_p, overallBenefit = modular_modular(graph, selectAlpha3, upperbound_2, S_r, k, benefits, influencedbenefits, Rw, Rz)
    # print("objective: " + str(overallBenefit))
    # S_p, overallBenefit = modular_modular(graph, selectAlpha4, upperbound_2, S_r, k, benefits, influencedbenefits, Rw, Rz)
    # print("objective: " + str(overallBenefit))

    delta = 0.1
    # k = 30
    # print("greedy")
    # S_p, overallBenefit = greedy(graph, S_r, k, benefits, influencedbenefits, Rw, Rz)
    # print("maxInf")
    # S_p, overallBenefit = maxInf(graph, S_r, k, benefits, influencedbenefits, Rw, Rz)
    # print("random")
    # S_p, overallBenefit = randomm(graph, S_r, k, benefits, influencedbenefits, Rw, Rz)
    # print("maxDegree")
    # S_p, overallBenefit = maxDegree(graph, S_r, k, benefits, influencedbenefits, Rw, Rz)
    # print("---------------------------------------")

    # K = [5, 10, 15, 20, 25, 30]
    K = [20]
    for k in K:
        print("k = " + str(k))

        print("mod-1")
        time_start = time.time()
        S_p, overallBenefit = modular_modular(graph, selectAlpha2, upperbound_1, S_r, k, benefits, influencedbenefits, Rw, Rz)
        time_end = time.time()
        ratio = approximation(graph, selectAlpha2, S_p, S_r, k, benefits, influencedbenefits, Rw, Rz, delta)
        print("objective: " + str(overallBenefit))
        print("ratio: " + str(ratio))
        print("time: " + str(time_end - time_start))

        print("mod-2")
        time_start = time.time()
        S_p, overallBenefit = modular_modular(graph, selectAlpha2, upperbound_2, S_r, k, benefits, influencedbenefits, Rw, Rz)
        time_end = time.time()
        ratio = approximation(graph, selectAlpha2, S_p, S_r, k, benefits, influencedbenefits, Rw, Rz, delta)
        print("objective: " + str(overallBenefit))
        print("ratio: " + str(ratio))
        print("time: " + str(time_end - time_start))

    # delta = 0.1
    # ratio = approximation(graph, selectAlpha2, upperbound_1, S_p, S_r, k, benefits, influencedbenefits, Rw, Rz, 0.1)
    # print(ratio)