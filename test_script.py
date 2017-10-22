from unweighted_graph import *

g_cyclic = UGraph({1:[5,2],2:[1,5,3],3:[2,4],4:[5,6],5:[1,4,2],6:[4]})
g_non_cyclic = UGraph({1:[2,3],2:[1,4],3:[1,5],4:[2],5:[3]})

print "graph cyclic",g_cyclic.isCyclic()
print "graph non cyclic",g_non_cyclic.isCyclic()

print g_cyclic.findPath(1, 6)
print g_cyclic.bestPath(1,6)

