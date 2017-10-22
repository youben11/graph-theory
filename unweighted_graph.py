""" Unweighted Graph Module.
    Graphs are represented as a dictionary,
    each node 'n' is a key which contain 
    a list of nodes that are reachable from
    that node 'n'."""

class UGraph(object):
    """ Unweighted Graph implementation """
    def __init__(self, graph):
        self.graph = graph
        self.is_cyclic = None
        
    def isCyclic(self):
        """ Check if the graph has a cycle or not """
        nodes = {i:None for i in self.graph.keys()} 
        nodes[nodes.keys()[0]] = 0
        fifo = [nodes.keys()[0]]
        
        while len(fifo) != 0:
            node = fifo.pop()
            for n in self.graph[node]:
                if nodes[n] >= nodes[node]:
                    self.is_cyclic = True
                    return True
                    
                elif nodes[n] == None:
                    nodes[n] = nodes[node] + 1
                    fifo.insert(0, n)
        self.is_cyclic = False
        return False
                        
    def setGraph(self, graph):
        self.graph = graph
        self.is_cyclic = None
        
    def bestPath(self, n_from, n_to):
        levels = self.bfs(n_from)
        level = 0
        found = False
        path = []
        
        while not found:
            # we are in the good level
            if n_to in levels[level].keys():
                found = True
                path.append(n_to)
                level -= 1
                child = n_to
                
                while level >= 0:
                    child = levels[level+1][child]
                    path.append(child)
                    level -=1
            # go to the next level
            else:
                level += 1
                
        return path[::-1]
        
    def bfs(self, n_from):
    
        nodes = {i:False for i in self.graph.keys()} # node:visited?
        nodes[n_from] = True
        fifo = [[n_from,],]
        level = 0
        n_by_level = [{n_from: None}] # (node, parent)
        all_visited = False
        
        while not all_visited :
            all_visited = True
            l_node = fifo[level]
            l = {}
            
            for node in l_node:
                for n in self.graph[node]:
                    if not nodes[n]: #not visited
                        all_visited = False
                        nodes[n] = True
                        l[n] = node

            if len(l) != 0:
                fifo.append([i for i in l.keys()])              
                level += 1
                n_by_level.append(l)

        return n_by_level
        
    def findPath(self, n_from, n_to):
      
        paths = []        
        nodes = {i:False for i in self.graph.keys()}
        nodes[n_from] = True
        
        for n in self.graph[n_from]:
            if not nodes[n]:
                path = [n_from]
                pos = self.dfs(self.graph, nodes, n)
                
                for p in pos:
                    if n_to in p:
                        paths.append(path + p[:p.index(n_to)+1])
                        return paths
        return []                        
                        
    @staticmethod
    def dfs(graph, states, node):
        states[node] = True
        paths = []
        
        for n in graph[node]:
            if not states[n]:
                path = [node]
                pos = UGraph.dfs(graph, states, n)
                
                for p in pos:
                    paths.append(path + p) 
                                       
        if len(paths) == 0:
            return [[node,],]
        else:
            return paths

                
            

        
    
        
