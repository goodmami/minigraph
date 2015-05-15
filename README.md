# minigraph

Small Python module for small graph structures

### Motivation

I [work with](https://github.com/goodmami/pydelphin) small graphs. I
build them programatically from other representations. I don't work with
huge graphs with millions of nodes and edges, but usually those with
less than 100. I want this in a graphing library:

  - it is fast to build graphs and make subgraphs
  - it is easy to query for basic properties, like size
  - it is fast to determine if a graph is connected or not
  - it is easy to do pathfinding
  - one graph type handles directed edges, undirected edges,
    labeled edges, and overlapping edges (multigraphs)
  - ideally it is a single file, so I can just copy it into other
    projects instead of making a dependency, which means...
  - it has a permissive open-source license

Consider some of the existing Python libraries for graphs:

  - [NetworkX][] is featureful, but slow
  - [graph-tool][] is fast, but GPL'd (it's based on the
    [Boost Graph Library][], which has a permissive license, but the
    author of graph-tool [seems uninterested in changing
    graph-tool's license](https://git.skewed.de/count0/graph-tool/issues/194))
  - [NetworKit][] is supposedly fast (though its hard to find any
    benchmarks to support this claim), and there's little documentation
    for building graphs programatically.

### Benchmarks

I compared MiniGraph to NetworkX. It's not directly comparable, because
the single MiniGraph class can be like NetworkXs Graph, DiGraph,
MultiGraph, and MultiDiGraph classes. Because of this, I compare it to
all of them. Here's the current state (times are in seconds):

    Building a chain of 100 nodes 10000 times:
      MiniGraph (regular   ) : 2.078411
      MiniGraph (fast_init ) : 1.903894
      NetworkX Graph         : 2.422691
      NetworkX DiGraph       : 3.009594
      NetworkX MultiGraph  : 4.788977
      NetworkX MultiDiGraph  : 5.369203
    Building a fully-connected 10-node graph 10000 times:
      MiniGraph (regular   ) : 1.174832
      MiniGraph (fast_init ) : 1.014850
      NetworkX Graph     : 1.749765
      NetworkX DiGraph     : 1.912611
      NetworkX MultiGraph: 4.029920
      NetworkX MultiDiGraph: 4.320380
    Building a 4x-connected 5x5-node graph 10000 times:
      MiniGraph (regular   ) : 1.068538
      MiniGraph (fast_init ) : 0.902589
      NetworkX MultiGraph: 3.878337
      NetworkX MultiDiGraph: 4.003757

A good start, but there's more work to do.

[NetworkX]: https://networkx.github.io/
[graph-tool]: https://graph-tool.skewed.de/
[Boost Graph Library]: http://www.boost.org/doc/libs/release/libs/graph
[NetworKit]: https://networkit.iti.kit.edu/