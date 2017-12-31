""" Weighted Graph Module.
    Graphs are represented as a dictionary,
    each node 'n' is a key which contain
    a list of nodes (node_value, weight) that are reachable from
    that node 'n'."""
from copy import deepcopy as dc

class WGraph(object):
    """ Weighted Graph implementation """
    def __init__(self, graph):
        self.graph = graph
        self.is_cyclic = None

    def setGraph(self, graph):
        self.graph = graph
        self.is_cyclic = None

    def unoriented(self):
        #Create a corresponding unoriented graph
        unoriented_g = dc(self.graph)
        for r in unoriented_g.keys():
            for n in unoriented_g[r]:
                found = False
                for m in unoriented_g[n[0]]:
                    if m[0] == r:
                        found = True
                if not found:
                    unoriented_g[n[0]].append((r,None))

        return unoriented_g

    def isCyclic(self):
        """ Check if the graph has a cycle or not """
        #Create a corresponding unoriented graph
        unoriented_g = self.unoriented()

        nodes = {i:None for i in self.graph.keys()}
        nodes[nodes.keys()[0]] = 0
        fifo = [nodes.keys()[0]]

        while len(fifo) != 0:
            node = fifo.pop()

            for n in [m[0] for m in unoriented_g[node]]:
                if nodes[n] >= nodes[node]:
                    self.is_cyclic = True
                    return True

                elif nodes[n] == None:
                    nodes[n] = nodes[node] + 1
                    fifo.insert(0, n)

        self.is_cyclic = False
        return False

    def kruskal(self):
        #get all edges with their weights
        edges = []
        for p in self.graph.keys():
            for n in self.graph[p]:
                edges.append((p,n[0],n[1]))

        m = len(edges)
        n = len(self.graph.keys())
        edges = sorted(edges, key=lambda x: x[2])
        f = []

        k = {key:[] for key in self.graph.keys()}

        for e in edges:
            if e[0] not in f or e[1] not in f:
                k[e[0]].append((e[1],e[2]))
                f.append(e[0])
                f.append(e[1])

            if len(f) > n-1:
                break

        return WGraph(k)

    def prim(self):

        unoriented_g = self.unoriented()

        v = self.graph.keys()
        u = [self.graph.keys()[0],]
        f = []

        while len(v) != len(u):
            edges = []
            for p in u:
                for n in self.graph[p]:
                    if n[0] not in u:
                        edges.append((p,n[0],n[1]))
            edges = sorted(edges, key=lambda x: x[2])
            f.append(edges[0])
            u.append(edges[0][1])

        n_graph = {key:[] for key in u}
        for e in f:
            n_graph[e[0]].append((e[1], e[2]))

        return WGraph(n_graph)

    def dijkstra(self, root):
        graph = self.graph
        for childs in graph.values():
            for c in childs:
                if c[1] < 0:
                    raise Exception("Negative weight")

        length = len(graph.keys())
        paths = {root: (root, 0)}
        visited = set([root,])
        curr = root
        cmp = {}

        while len(visited) != length:
            childs = graph[curr]
            for c in childs:
                if c[0] not in visited:
                    if c[0] not in cmp.keys():
                        cmp[c[0]] = (curr, c[1] + paths[curr][1])
                    elif cmp[c[0]][1] > c[1] + paths[curr][1]:
                        cmp[c[0]] = (curr, c[1] + paths[curr][1])

            sor = sorted([i for i in zip(cmp.keys(), cmp.values())],\
                         key=lambda t:t[1])
            curr = sor[-1]
            paths[curr[0]] = (curr[1][0], curr[1][1])

            curr = curr[0]
            visited.add(curr)
            del(cmp[curr])

        result = {}
        for p in paths.keys():
            tmp = [p,]
            c = paths[p]
            while True:
                tmp.append(c[0])
                if c[0] == root:
                    break
                c = paths[c[0]]
            result[p] = (list(set(tmp[::-1])), paths[p][1])

        return result

    def bellman_ford(self, root):
        graph = self.graph

        length = len(graph.keys())
        paths = {root: (root, 0)}
        curr = root
        cmp = paths
        count = 0
        old = {}

        while old != cmp:#len(visited) != lengt:
            old = dc(cmp)
            count += 1
            if count > len(graph.keys()):
                raise Exception("Circuit detected")

            for curr in graph.keys():
                childs = graph[curr]
                for c in childs:
                    if c[0] not in cmp.keys():
                        cmp[c[0]] = (curr, c[1] + paths[curr][1])
                    elif cmp[c[0]][1] > c[1] + paths[curr][1]:
                        cmp[c[0]] = (curr, c[1] + paths[curr][1])

        result = {}
        for p in paths.keys():
            tmp = [p,]
            c = paths[p]
            while True:
                tmp.append(c[0])
                if c[0] == root:
                    break
                c = paths[c[0]]
            result[p] = (tmp[::-1], paths[p][1])

        return result
