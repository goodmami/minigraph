
import timeit

print('Building a chain of 100 nodes 10000 times:')

t = timeit.timeit(
    stmt='mg.MiniGraph(edges=edges)',
    setup='import minigraph as mg; edges = [(i, i+1, None, {}, True) for i in range(100)]',
    number=10000)
print('  MiniGraph (regular   ) : %f' % t)

t = timeit.timeit(
    stmt='mg.MiniGraph.fast_init(edges=edges)',
    setup='import minigraph as mg; edges = [(i, i+1, None, {}, True) for i in range(100)]',
    number=10000)
print('  MiniGraph (fast_init ) : %f' % t)

# t = timeit.timeit(
#     stmt='mg.MiniGraph.fast_init2(nodes, edges=edges)',
#     setup='import minigraph as mg; nodes=range(101); edges = [(i, i+1, None, {}, True) for i in range(100)]',
#     number=10000)
# print('  MiniGraph (fast_init2) : %f' % t)

t = timeit.timeit(
    stmt='nx.Graph(edges)',
    setup='import networkx as nx; edges = [(i, i+1) for i in range(100)]',
    number=10000
)
print('  NetworkX Graph         : %f' % t)

t = timeit.timeit(
    stmt='nx.DiGraph(edges)',
    setup='import networkx as nx; edges = [(i, i+1) for i in range(100)]',
    number=10000
)
print('  NetworkX DiGraph       : %f' % t)

t = timeit.timeit(
    stmt='nx.MultiGraph(edges)',
    setup='import networkx as nx; edges = [(i, i+1) for i in range(100)]',
    number=10000
)
print('  NetworkX MultiGraph  : %f' % t)

t = timeit.timeit(
    stmt='nx.MultiDiGraph(edges)',
    setup='import networkx as nx; edges = [(i, i+1) for i in range(100)]',
    number=10000
)
print('  NetworkX MultiDiGraph  : %f' % t)


print('Building a fully-connected 10-node graph 10000 times:')

t = timeit.timeit(
    stmt='mg.MiniGraph(edges=edges)',
    setup='import minigraph as mg; edges = [(i, j, None, {}, True) for i in range(10) for j in range(10)]',
    number=10000)
print('  MiniGraph (regular   ) : %f' % t)

t = timeit.timeit(
    stmt='mg.MiniGraph.fast_init(edges=edges)',
    setup='import minigraph as mg; edges = [(i, j, None, {}, True) for i in range(10) for j in range(10)]',
    number=10000)
print('  MiniGraph (fast_init ) : %f' % t)

# t = timeit.timeit(
#     stmt='mg.MiniGraph.fast_init2(nodes, edges=edges)',
#     setup='import minigraph as mg; nodes=range(10); edges = [(i, j, None, {}, True) for i in range(10) for j in range(10)]',
#     number=10000)
# print('  MiniGraph (fast_init2) : %f' % t)

t = timeit.timeit(
    stmt='nx.Graph(edges)',
    setup='import networkx as nx; edges = [(i, j) for i in range(10) for j in range(10)]',
    number=10000
)
print('  NetworkX Graph     : %f' % t)

t = timeit.timeit(
    stmt='nx.DiGraph(edges)',
    setup='import networkx as nx; edges = [(i, j) for i in range(10) for j in range(10)]',
    number=10000
)
print('  NetworkX DiGraph     : %f' % t)

t = timeit.timeit(
    stmt='nx.MultiGraph(edges)',
    setup='import networkx as nx; edges = [(i, j) for i in range(10) for j in range(10)]',
    number=10000
)
print('  NetworkX MultiGraph: %f' % t)

t = timeit.timeit(
    stmt='nx.MultiDiGraph(edges)',
    setup='import networkx as nx; edges = [(i, j) for i in range(10) for j in range(10)]',
    number=10000
)
print('  NetworkX MultiDiGraph: %f' % t)


print('Building a 4x-connected 5x5-node graph 10000 times:')

t = timeit.timeit(
    stmt='mg.MiniGraph(edges=edges)',
    setup='import minigraph as mg; edges = [(i, j, l, {}, True) for l in ("one", "two", "three", "four") for i in range(5) for j in range(5)]',
    number=10000)
print('  MiniGraph (regular   ) : %f' % t)

t = timeit.timeit(
    stmt='mg.MiniGraph.fast_init(edges=edges)',
    setup='import minigraph as mg; edges = [(i, j, l, {}, True) for l in ("one", "two", "three", "four") for i in range(5) for j in range(5)]',
    number=10000)
print('  MiniGraph (fast_init ) : %f' % t)

# t = timeit.timeit(
#     stmt='mg.MiniGraph.fast_init2(nodes, edges=edges)',
#     setup='import minigraph as mg; nodes=range(5); edges = [(i, j, l, {}, True) for l in ("one", "two", "three", "four") for i in range(5) for j in range(5)]',
#     number=10000)
# print('  MiniGraph (fast_init2) : %f' % t)

t = timeit.timeit(
    stmt='nx.MultiGraph(edges)',
    setup='import networkx as nx; edges = [(i, j, {"label": l}) for l in ("one", "two", "three", "four") for i in range(5) for j in range(5)]',
    number=10000
)
print('  NetworkX MultiGraph: %f' % t)

t = timeit.timeit(
    stmt='nx.MultiDiGraph(edges)',
    setup='import networkx as nx; edges = [(i, j, {"label": l}) for l in ("one", "two", "three", "four") for i in range(5) for j in range(5)]',
    number=10000
)
print('  NetworkX MultiDiGraph: %f' % t)

# print('Retrieving nodes from the 10-node graph 10000 times:')

# t = timeit.timeit(
#     stmt='g.node(5)',
#     setup='import minigraph as mg; '
#           'edges = [(i, j, l, {}, True) for l in ("one", "two", "three", "four") '
#           'for i in range(10) for j in range(5)]; '
#           'g = mg.MiniGraph(edges=edges)',
#     number=10000)
# print('  MiniGraph (directed) : %f' % t)

# print('Retrieving edges from the 10-node graph 10000 times:')

# t = timeit.timeit(
#     stmt='g.edge(1,4,"one")',
#     setup='import minigraph as mg; '
#           'edges = [(i, j, l, {}, True) for l in ("one", "two", "three", "four") '
#           'for i in range(10) for j in range(5)]; '
#           'g = mg.MiniGraph(edges=edges)',
#     number=10000)
# print('  MiniGraph (directed) : %f' % t)
