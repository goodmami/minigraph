
import warnings

class MiniGraphError(Exception): pass
class MiniGraphWarning(Warning): pass

# todo: consider functools.lru_cache for the retrieval methods

class MiniGraph(object):

    __slots__ = ('nodes', 'edges', '_edges', 'uedges')

    def __init__(self, nodes=None, edges=None):

        # nodes
        self.nodes = {}
        for node in (nodes or []):
            try:
                node, data = node
            except TypeError:
                data = {}
            self.add_node(node, data=data)

        # edges
        self.edges = {}  # directed edges
        self._edges = {}  # cache for reverse-lookup of directed edges
        self.uedges = {}  # undirected edges
        self.add_edges(edges or [])

    def __getitem__(self, idx):
        """
        Fancy graph queries:
          - if idx is an integer, return the node given by idx
          - if idx is a slice, return the edges matching
            start:end:label. Note that not specifying the label uses
            the label of None, which is a valid label. If you want to
            consider all labels, use Ellipsis: (g[0:1:...]). All edges
            can be retrieved with g[::...].
        """

        try:
            start, end, label = idx.start, idx.stop, idx.step
            if label is Ellipsis:
                return self.find_edges(start, end)
            else:
                return self.find_edges(start, end, label=label)
        except AttributeError:
            return (idx, self.nodes[idx])

    def add_node(self, nodeid, data=None):
        if nodeid in self.nodes:
            raise MiniGraphError('Node already exists: {}'.format(nodeid))
        self.nodes[nodeid] = dict(data or [])

    def remove_node(self, nodeid):
        self.nodes[nodeid]  # check for KeyError
        _prune_edges(self, nodeid)
        del self.nodes[nodeid]

    def node(self, key):
        return self.nodes[key]

    def add_edge(self, start, end, label=None, data=None, directed=True):
        self.add_edges([(start, end, label, data, directed)])

    def add_edges(self, edges):
        nodes = self.nodes

        for edge in edges:
            edgelen = len(edge)
            if edgelen == 5:
                start, end, label, dat, directed = edge
            elif edgelen == 4:
                start, end, label, dat = edge; directed = True
            elif edgelen == 3:
                start, end, label = edge; dat = None; directed = True
            elif edgelen == 2:
                start, end = edge; label = dat = None; directed = True
            else:
                raise MiniGraphError('Invalid edge: {}'.format(edge))

            data = {}
            if dat is not None:
                data.update(dat)

            if start not in nodes:
                nodes[start] = {}
            if end not in nodes:
                nodes[end] = {}

            # directed edges have a reverse lookup; undirected edges just put
            # each edge in the same dict twice
            if directed is False:
                edges = self.uedges
                redges = self.uedges
            else:
                edges = self.edges
                redges = self._edges

            if start not in edges:
                edges[start] = {label: {end: data}}
            else:
                startdict = edges[start]
                if label not in startdict:
                    startdict[label] = {end: data}
                else:
                    startdict[label][end] = data

            if end not in redges:
                redges[end] = {label: {start: data}}
            else:
                enddict = redges[end]
                if label not in enddict:
                    enddict[label] = {start: data}
                else:
                    enddict[label][start] = data

    def remove_edge(self, start, end, label=None, directed=True):
        # first check for KeyError
        if directed:
            self.edges[start][label][end]
        else:
            self.uedges[start][label][end]
        # now attempt to remove
        try:
            if directed:
                del self.edges[start][label][end]
                _cleanup_edgedict(self.edges, start, label)
                del self._edges[end][label][start]
                _cleanup_edgedict(self._edges, end, label)
            else:
                del self.uedges[start][label][end]
                _cleanup_edgedict(self.uedges, start, label)
                # it's possible for an undirected loop to only have one
                # entry, so don't remove twice if they are the same
                if end != start:
                    del self.uedges[end][label][start]
                    _cleanup_edgedict(self.uedges, end, label)
        except KeyError:
            warnings.warn(
                'Unexpected KeyError while removing {} edge ({}, {}, {})'
                .format('directed' if directed else 'undirected',
                        start, end, label),
                MiniGraphWarning
            )

    def edge(self, start, end, label=None, directed=True):
        if directed:
            return self.edges[start][label][end]
        else:
            return self.uedges[start][label][end]

    def find_edges(self, start=None, end=None, **kwargs):
        if start is Ellipsis: start = None
        if end is Ellipsis: end = None

        # get appropriate edge dicts (both if 'directed' is unspecified)
        if 'directed' in kwargs:
            if kwargs['directed'] is True: xs = [self.edges]
            elif kwargs['directed'] is False: xs = [self.uedges]
            else: xs = [self.edges, self.uedges]

        # filter by start, if specified
        if start is None:
            xs = [(s, sd) for d in xs for s, sd in d.items()]
        else:
            xs = [(start, d[start]) for d in xs if start in d]

        # filter by label, if specified
        try:
            lbl = kwargs['label']
            xs = ((s, lbl, sd[lbl]) for s, sd in xs if lbl in sd)
        except KeyError:
            xs = ((s, lbl, ld) for s, sd in xs for lbl, ld in sd.items())

        # filter by end, if specified
        if end is None:
            xs = ((s, e, lbl, d) for s, lbl, ld in xs for e, d in ld.items())
        else:
            xs = ((s, end, lbl, ld[end]) for s, lbl, ld in xs if end in ld)

        # filter by data, if specified
        try:
            data = kwargs['data']
            xs = filter(
                lambda s,e,l,d: all(d.get(k) == v for k, v in data.items()),
                xs
            )
        except KeyError:
            pass

        return list(xs)

    def order(self):
        return len(self.nodes)

    def size(self):
        return (
            sum(len(ed)
                for ld in self.edges.values()
                for ed in ld.values()) +
            # undirected edges are in uedges twice, except for undirected
            # simple loops
            (sum(1 if e != s else 2
                 for s, ld in self.uedges.items()
                 for ed in ld.values()
                 for e in ed.keys()) / 2)
        )

    def degree(self, nodeid):
        self.nodes[nodeid]  # check for KeyError
        return _degree(nodeid, [self.edges, self._edges, self.uedges])

    def out_degree(self, nodeid):
        self.nodes[nodeid]  # check for KeyError
        return _degree(nodeid, [self.edges, self.uedges])

    def in_degree(self, nodeid):
        self.nodes[nodeid]  # check for KeyError
        return _degree(nodeid, [self._edges, self.uedges])

    def subgraph(self, nodeids):
        nidset = set(nodeids)
        nodes = self.nodes
        edges = self.edges
        uedges = self.uedges
        all_edges = [
            (start, end, label, ld[end])
            for start in nodeids
            for label, ld in edges.get(start, {}).items()
            for end, edgedata in ld.items() if end in nidset
        ] + [
            (start, end, label, ld[end], False)
            for start in nodeids
            for label, ld in uedges.get(start, {}).items()
            for end, edgedata in ld.items() if end in nidset
        ]
        return MiniGraph(
            nodes=[(nid, nodes[nid]) for nid in nodeids],
            edges=all_edges
        )

    # def connected(self):
    #     nodeset = set()
    #     remaining = set(self.nodes.keys())

    #     for start in self.nodes:
    #         if node not in nodeset:
    #             nodeset.add(node)

def _degree(nodeid, edgedicts):
    ds = []
    for d in edgedicts:
        if nodeid in d:
            ds.append(d[nodeid])
    return sum(len(ld) for d in ds for ld in d.values())

def _prune_edges(graph, nodeid):
    # for efficiency, I don't use MiniGraph.remove_edge inside the loop
    es = graph.edges
    _es = graph._edges
    ues = graph.uedges
    for d1, d2, dir_ in ((es, _es, True), (_es, es, True), (ues, ues, False)):
        if nodeid not in d1:
            continue
        for lbl, ld in d1[nodeid].items():
            for end in ld.keys():
                if end == nodeid:  # this will get pruned anyway
                    continue
                try:
                    del d2[end][lbl][nodeid]
                    # can this be moved outside the loop?
                    _cleanup_edgedict(d2, end, lbl)
                except KeyError:
                    warnings.warn(
                        'Unexpected KeyError while removing {} edge '
                        '({}, {}, {})'
                        .format('directed' if dir_ else 'undirected',
                                nodeid, end, lbl),
                        MiniGraphWarning
                    )
        del d1[nodeid]

def _cleanup_edgedict(edgedict, start, label):
    if len(edgedict[start][label]) == 0:
        del edgedict[start][label]
    if len(edgedict[start]) == 0:
        del edgedict[start]
