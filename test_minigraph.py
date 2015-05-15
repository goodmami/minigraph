import pytest

import minigraph as mg

def esort(es):
    return sorted(es, key=lambda e: (e[0], e[1], e[2] is not None, e[2]))

def test_simple_init():
    g = mg.MiniGraph()
    assert g.nodes() == []
    assert g.edges() == []

    g = mg.MiniGraph([1])
    assert g.nodes() == [(1, {})]
    assert g.edges() == []

    g = mg.MiniGraph([(1, {'attr': 'val'})])
    assert g.nodes() == [(1, {'attr': 'val'})]
    assert g.edges() == []

    g = mg.MiniGraph([(1, {'attr': 'val'}), 2])
    assert sorted(g.nodes()) == [(1, {'attr': 'val'}), (2, {})]
    assert g.edges() == []

    # with pytest.raises(mg.MiniGraphError):
    #     mg.MiniGraph([1, 1])

def test_directed_init():
    # basic directed
    g = mg.MiniGraph([1,2], [(1, 2)])
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert g.edges() == [(1, 2, None, {}, True)]

    # basic directed with auto-populated nodes
    g = mg.MiniGraph(edges=[(1, 2)])
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert g.edges() == [(1, 2, None, {}, True)]

    # basic with label
    g = mg.MiniGraph([1,2], [(1, 2, 'label')])
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert g.edges() == [(1, 2, 'label', {}, True)]

    # basic with data
    g = mg.MiniGraph([1,2], [(1, 2, None, {'attr': 'val'})])
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert g.edges() == [(1, 2, None, {'attr': 'val'}, True)]

    # from here assume g.uedges is {}

    # multiple same source
    g = mg.MiniGraph([1,2,3], [(1, 2), (1, 3)])
    assert sorted(g.nodes()) == [(1, {}), (2, {}), (3, {})]
    assert esort(g.edges()) == [(1, 2, None, {}, True),
                                 (1, 3, None, {}, True)]

    # multiple same target
    g = mg.MiniGraph([1,2,3], [(1, 2), (3, 2)])
    assert sorted(g.nodes()) == [(1, {}), (2, {}), (3, {})]
    assert esort(g.edges()) == [(1, 2, None, {}, True),
                                 (3, 2, None, {}, True)]

    # cycle
    g = mg.MiniGraph([1,2], [(1, 2), (2, 1)])
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert esort(g.edges()) == [(1, 2, None, {}, True),
                                 (2, 1, None, {}, True)]

    # simple loop
    g = mg.MiniGraph([1], [(1, 1)])
    assert g.nodes() == [(1, {})]
    assert g.edges() == [(1, 1, None, {}, True)]

    # cannot have same edge with same label (see labeled tests below)
    # with pytest.raises(mg.MiniGraphError):
    #     mg.MiniGraph([1, 2], [(1, 2), (1, 2)])


def test_undirected_init():
    # basic undirected
    g = mg.MiniGraph([1,2], [(1, 2, None, None, False)])
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert g.edges() == [(1, 2, None, {}, False)]

    # basic undirected with auto-populated nodes
    g = mg.MiniGraph(edges=[(1, 2, None, None, False)])
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert g.edges() == [(1, 2, None, {}, False)]

    # basic with label
    g = mg.MiniGraph([1,2], [(1, 2, 'label', None, False)])
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert g.edges() == [(1, 2, 'label', {}, False)]

    # basic with data
    g = mg.MiniGraph([1,2], [(1, 2, None, {'attr': 'val'}, False)])
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert g.edges() == [(1, 2, None, {'attr': 'val'}, False)]

    # multiple same source
    g = mg.MiniGraph(
        [1,2,3],
        [(1, 2, None, None, False), (1, 3, None, None, False)]
    )
    assert sorted(g.nodes()) == [(1, {}), (2, {}), (3, {})]
    assert esort(g.edges()) == [(1, 2, None, {}, False),
                                 (1, 3, None, {}, False)]

    # multiple same target
    g = mg.MiniGraph(
        [1,2,3],
        [(1, 2, None, None, False), (3, 2, None, None, False)]
    )
    assert sorted(g.nodes()) == [(1, {}), (2, {}), (3, {})]
    assert esort(g.edges()) == [(1, 2, None, {}, False),
                                 (3, 2, None, {}, False)]

    # cycle in args raises error
    # with pytest.raises(mg.MiniGraphError):
    #     mg.MiniGraph(
    #         [1,2],
    #         [(1, 2, None, None, False), (2, 1, None, None, False)]
    #     )

    # simple loops are ok
    g = mg.MiniGraph([1], [(1, 1, None, None, False)])
    assert g.edges() == [(1, 1, None, {}, False)]

    # cannot have same edge with same label (see labeled tests below)
    # with pytest.raises(mg.MiniGraphError):
    #     mg.MiniGraph(
    #         [1, 2],
    #         [(1, 2, None, None, False), (1, 2, None, None, False)]
    #     )

def test_add_node():
    g = mg.MiniGraph()
    assert g.nodes() == []
    g.add_node(1)
    assert g.nodes() == [(1, {})]
    # with pytest.raises(mg.MiniGraphError):
    #     g.add_node(1)
    g.add_node(2, data={'attr': 'val'})
    assert sorted(g.nodes()) == [(1, {}), (2, {'attr': 'val'})]

def test_remove_node():
    g = mg.MiniGraph(edges=[(1,2), (2,3), (3,1), (1,1)])
    assert sorted(g.nodes()) == [(1, {}), (2, {}), (3, {})]
    g.remove_node(1)
    assert sorted(g.nodes()) == [(2, {}), (3, {})]
    assert g.edges() == [(2, 3, None, {}, True)]
    with pytest.raises(KeyError):
        g.remove_node(1)

def test_add_edge():
    g = mg.MiniGraph()
    assert g.edges() == []
    g.add_edge(1, 2)
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert g.edges() == [(1, 2, None, {}, True)]
    # with pytest.raises(mg.MiniGraphError):
    #     g.add_edge(1, 2)
    g.add_edge(1, 2, label='label')
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert esort(g.edges()) == [(1, 2, None, {}, True),
                                 (1, 2, 'label', {}, True)]
    g = mg.MiniGraph()
    g.add_edge(1, 2, data={'attr': 'val'})
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert g.edges() == [(1, 2, None, {'attr': 'val'}, True)]
    g = mg.MiniGraph()
    g.add_edge(1, 2, directed=False)
    assert sorted(g.nodes()) == [(1, {}), (2, {})]
    assert g.edges() == [(1, 2, None, {}, False)]
    g = mg.MiniGraph()
    g.add_edge(1, 1)
    assert g.nodes() == [(1, {})]
    assert g.edges() == [(1, 1, None, {}, True)]

def test_remove_edge():
    g = mg.MiniGraph(edges=[(1,2), (2,1)])
    assert esort(g.edges()) == [(1, 2, None, {}, True),
                                 (2, 1, None, {}, True)]
    with pytest.raises(KeyError):
        g.remove_edge(1, 4)
    assert esort(g.edges()) == [(1, 2, None, {}, True),
                                 (2, 1, None, {}, True)]
    g.remove_edge(1, 2)
    assert g.edges() == [(2, 1, None, {}, True)]
    with pytest.raises(KeyError):
        g.remove_edge(1, 2)

    g = mg.MiniGraph(edges=[(1,1), (1,1,'other')])
    assert esort(g.edges()) == [(1, 1, None, {}, True),
                                 (1, 1, 'other', {}, True)]
    g.remove_edge(1, 1)
    assert g.edges() == [(1, 1, 'other', {}, True)]
    g = mg.MiniGraph(edges=[(1,1), (1,1,'other')])
    g.remove_edge(1, 1, label='other')
    assert g.edges() == [(1, 1, None, {}, True)]

    g = mg.MiniGraph(edges=[(1,1,'dir'), (1,1,'und',None,False)])
    assert esort(g.edges()) == [(1, 1, 'dir', {}, True),
                                (1, 1, 'und', {}, False)]
    g.remove_edge(1, 1, 'dir', directed=True)
    assert g.edges() == [(1, 1, 'und', {}, False)]
    g = mg.MiniGraph(edges=[(1,1,'dir'), (1,1,'und',None,False)])
    g.remove_edge(1, 1, 'und', directed=False)
    assert g.edges() == [(1, 1, 'dir', {}, True)]

    g = mg.MiniGraph(edges=[(1,2,None,None,False)])
    assert g.edge(1,2) is not None
    assert g.edge(2,1) is not None
    g.remove_edge(1, 2)
    with pytest.raises(KeyError):
        g.edge(1,2)
    with pytest.raises(KeyError):
        g.edge(2,1)
    g = mg.MiniGraph(edges=[(1,2,None,None,False)])
    assert g.edge(1,2) is not None
    assert g.edge(2,1) is not None
    g.remove_edge(2, 1)
    with pytest.raises(KeyError):
        g.edge(1,2)
    with pytest.raises(KeyError):
        g.edge(2,1)

def test_node():
    pass

def test_edge():
    pass

def test_find_edges():
    pass

def test_order():
    assert mg.MiniGraph().order() == 0
    assert mg.MiniGraph([1]).order() == 1
    assert mg.MiniGraph([1,2]).order() == 2
    assert mg.MiniGraph([1,2], [(1,2)]).order() == 2

def test_size():
    # no edges
    assert mg.MiniGraph().size() == 0
    assert mg.MiniGraph([1,2,3]).size() == 0
    # basic edges
    assert mg.MiniGraph(edges=[(1,2)]).size() == 1
    assert mg.MiniGraph(edges=[(1,2,'label')]).size() == 1
    # overlapping edges
    assert mg.MiniGraph(edges=[(1,2),(1,2,'label')]).size() == 2
    # cycles and loops
    assert mg.MiniGraph(edges=[(1,2),(2,1)]).size() == 2
    assert mg.MiniGraph(edges=[(1,1)]).size() == 1
    # undirected
    assert mg.MiniGraph(edges=[(1,1,None,None,False)]).size() == 1
    assert mg.MiniGraph(edges=[(1,2,None,None,False)]).size() == 1

def test_out_degree():
    with pytest.raises(KeyError):
        mg.MiniGraph().out_degree(0)
    assert mg.MiniGraph([1]).out_degree(1) == 0
    # basic directed
    g = mg.MiniGraph(edges=[(1,2)])
    assert g.out_degree(1) == 1
    assert g.out_degree(2) == 0
    # directed cycle
    g = mg.MiniGraph(edges=[(1,2), (2,1)])
    assert g.out_degree(1) == 1
    assert g.out_degree(2) == 1
    # directed same source
    g = mg.MiniGraph(edges=[(1,2), (1,3)])
    assert g.out_degree(1) == 2
    assert g.out_degree(2) == 0
    assert g.out_degree(3) == 0
    # directed simple loop
    g = mg.MiniGraph(edges=[(1,1)])
    assert g.out_degree(1) == 1

    # basic undirected
    g = mg.MiniGraph(edges=[(1,2, None, None, False)])
    assert g.out_degree(1) == 1
    assert g.out_degree(2) == 1
    # undirected same source
    g = mg.MiniGraph(
        edges=[(1,2, None, None, False), (1,3, None, None, False)]
    )
    assert g.out_degree(1) == 2
    assert g.out_degree(2) == 1
    assert g.out_degree(3) == 1
    # undirected simple loop
    g = mg.MiniGraph(edges=[(1,1, None, None, False)])
    assert g.out_degree(1) == 1

def test_in_degree():
    with pytest.raises(KeyError):
        mg.MiniGraph().in_degree(0)
    assert mg.MiniGraph([1]).in_degree(1) == 0
    # basic directed
    g = mg.MiniGraph(edges=[(1,2)])
    assert g.in_degree(1) == 0
    assert g.in_degree(2) == 1
    # directed cycle
    g = mg.MiniGraph(edges=[(1,2), (2,1)])
    assert g.in_degree(1) == 1
    assert g.in_degree(2) == 1
    # directed same source
    g = mg.MiniGraph(edges=[(1,2), (1,3)])
    assert g.in_degree(1) == 0
    assert g.in_degree(2) == 1
    assert g.in_degree(3) == 1
    # directed same target
    g = mg.MiniGraph(edges=[(1,2), (3,2)])
    assert g.in_degree(1) == 0
    assert g.in_degree(2) == 2
    assert g.in_degree(3) == 0
    # directed simple loop
    g = mg.MiniGraph(edges=[(1,1)])
    assert g.in_degree(1) == 1

    # basic undirected
    g = mg.MiniGraph(edges=[(1,2, None, None, False)])
    assert g.in_degree(1) == 1 # 0
    assert g.in_degree(2) == 1 # 2
    # undirected same source
    g = mg.MiniGraph(
        edges=[(1,2, None, None, False), (1,3, None, None, False)]
    )
    assert g.in_degree(1) == 2
    assert g.in_degree(2) == 1
    assert g.in_degree(3) == 1
    # undirected same target
    g = mg.MiniGraph(
        edges=[(1,2, None, None, False), (3,2, None, None, False)]
    )
    assert g.in_degree(1) == 1
    assert g.in_degree(2) == 2
    assert g.in_degree(3) == 1

    # undirected simple loop
    g = mg.MiniGraph(edges=[(1,1, None, None, False)])
    assert g.in_degree(1) == 1

def test_degree():
    with pytest.raises(KeyError):
        mg.MiniGraph().degree(0)
    assert mg.MiniGraph([1]).degree(1) == 0
    # basic directed
    g = mg.MiniGraph(edges=[(1,2)])
    assert g.degree(1) == 1
    assert g.degree(2) == 1
    # directed cycle
    g = mg.MiniGraph(edges=[(1,2), (2,1)])
    assert g.degree(1) == 2
    assert g.degree(2) == 2
    # directed same source
    g = mg.MiniGraph(edges=[(1,2), (1,3)])
    assert g.degree(1) == 2
    assert g.degree(2) == 1
    assert g.degree(3) == 1
    # directed same target
    g = mg.MiniGraph(edges=[(1,2), (3,2)])
    assert g.degree(1) == 1
    assert g.degree(2) == 2
    assert g.degree(3) == 1
    # directed simple loop
    g = mg.MiniGraph(edges=[(1,1)])
    assert g.degree(1) == 2

    # basic undirected
    g = mg.MiniGraph(edges=[(1,2, None, None, False)])
    assert g.degree(1) == 1
    assert g.degree(2) == 1
    # undirected same source
    g = mg.MiniGraph(
        edges=[(1,2, None, None, False), (1,3, None, None, False)]
    )
    assert g.degree(1) == 2
    assert g.degree(2) == 1
    assert g.degree(3) == 1
    # undirected same target
    g = mg.MiniGraph(
        edges=[(1,2, None, None, False), (3,2, None, None, False)]
    )
    assert g.degree(1) == 1
    assert g.degree(2) == 2
    assert g.degree(3) == 1

    # undirected simple loop
    g = mg.MiniGraph(edges=[(1,1, None, None, False)])
    assert g.degree(1) == 2

def test_subgraph():
    with pytest.raises(KeyError):
        mg.MiniGraph([1]).subgraph([2])

    sg = mg.MiniGraph().subgraph([])
    assert len(sg.nodes()) == 0
    assert len(sg.edges()) == 0

    sg = mg.MiniGraph([1]).subgraph([])
    assert len(sg.nodes()) == 0
    assert len(sg.edges()) == 0

    sg = mg.MiniGraph([1]).subgraph([1])
    assert len(sg.nodes()) == 1
    assert len(sg.edges()) == 0

    g = mg.MiniGraph(edges=[(1,2),(2,3),(3,1)])
    sg = g.subgraph([1,2])
    assert sorted(sg.nodes()) == [(1, {}), (2, {})]
    assert sg.edges() == [(1, 2, None, {}, True)]

    sg = g.subgraph([1,3])
    assert sorted(sg.nodes()) == [(1, {}), (3, {})]
    assert sg.edges() == [(3, 1, None, {}, True)]

    g = mg.MiniGraph(edges=[(1,1),(1,1,'und',None,False)])
    sg = g.subgraph([1])
    assert sg.nodes() == [(1, {})]
    assert esort(sg.edges()) == [(1, 1, None, {}, True),
                                 (1, 1, 'und', {}, False)]

