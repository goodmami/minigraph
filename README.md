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
    it](https://git.skewed.de/count0/graph-tool/issues/194))
  - [NetworKit][] is supposedly fast (though its hard to find any
    benchmarks to support this claim), and there's little documentation
    for building graphs programatically.

[NetworkX]: https://networkx.github.io/
[graph-tool]: https://graph-tool.skewed.de/
[Boost Graph Library]: http://www.boost.org/doc/libs/release/libs/graph
[NetworKit]: https://networkit.iti.kit.edu/