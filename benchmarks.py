
import timeit

print('Building a chain of 100 nodes 10000 times:')

t = timeit.timeit(
    stmt='mg.MiniGraph(edges=edges)',
    setup='import minigraph as mg; edges = [(i, i+1) for i in range(100)]',
    number=10000)
print('  MiniGraph (directed) : %f' % t)

t = timeit.timeit(
    stmt='mg.MiniGraph(edges=edges)',
    setup='import minigraph as mg; edges = [(i, i+1, None, None, False) for i in range(100)]',
    number=10000)
print('  MiniGraph (undir)    : %f' % t)

t = timeit.timeit(
    stmt='nx.Graph(edges)',
    setup='import networkx as nx; edges = [(i, i+1) for i in range(100)]',
    number=10000
)
print('  NetworkX Graph       : %f' % t)

t = timeit.timeit(
    stmt='nx.DiGraph(edges)',
    setup='import networkx as nx; edges = [(i, i+1) for i in range(100)]',
    number=10000
)
print('  NetworkX DiGraph     : %f' % t)

t = timeit.timeit(
    stmt='nx.MultiDiGraph(edges)',
    setup='import networkx as nx; edges = [(i, i+1) for i in range(100)]',
    number=10000
)
print('  NetworkX MultiDiGraph: %f' % t)


print('Building a fully-connected 10-node graph 10000 times:')

t = timeit.timeit(
    stmt='mg.MiniGraph(edges=edges)',
    setup='import minigraph as mg; edges = [(i, j) for i in range(10) for j in range(20)]',
    number=10000)
print('  MiniGraph            : %f' % t)

t = timeit.timeit(
    stmt='nx.DiGraph(edges)',
    setup='import networkx as nx; edges = [(i, j) for i in range(10) for j in range(20)]',
    number=10000
)
print('  NetworkX DiGraph     : %f' % t)

t = timeit.timeit(
    stmt='nx.MultiDiGraph(edges)',
    setup='import networkx as nx; edges = [(i, j) for i in range(10) for j in range(20)]',
    number=10000
)
print('  NetworkX MultiDiGraph: %f' % t)
