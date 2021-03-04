def readRearrange(path):
    node = set()
    node_mapping = {}
    count = 1
    f = open(path, 'r')
    w = open("./soc-sign-bitcoinalpha.txt", 'w+')
    for line in f.readlines():
        line = line.strip()
        if not len(line) or line.startswith('#'):
            continue
        row = line.split(",")
        src = int(row[0])
        dst = int(row[1])
        if src in node:
            src = node_mapping[src]
        else:
            node.add(src)
            node_mapping[src] = count
            count += 1
            src = node_mapping[src]
        if dst in node:
            dst = node_mapping[dst]
        else:
            node.add(dst)
            node_mapping[dst] = count
            count += 1
            dst = node_mapping[dst]
        print(str(src) + " " + str(dst), file=w)


if __name__ == '__main__':
    path = "soc-sign-bitcoinalpha.csv"
    readRearrange(path)