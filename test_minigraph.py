import pytest

import minigraph as mg

def test_simple_init():
    g = mg.MiniGraph()
    assert g.nodes == {}
    assert g.edges == {}
    assert g._edges == {}
    assert g.uedges == {}

    g = mg.MiniGraph([1])
    assert g.nodes == {1: {}}
    assert g.edges == {}
    assert g._edges == {}
    assert g.uedges == {}

    g = mg.MiniGraph([(1, {'attr': 'val'})])
    assert g.nodes == {1: {'attr': 'val'}}
    assert g.edges == {}
    assert g._edges == {}
    assert g.uedges == {}

    g = mg.MiniGraph([(1, {'attr': 'val'}), 2])
    assert g.nodes == {1: {'attr': 'val'}, 2: {}}
    assert g.edges == {}
    assert g._edges == {}
    assert g.uedges == {}

    # with pytest.raises(mg.MiniGraphError):
    #     mg.MiniGraph([1, 1])

def test_directed_init():
    # basic directed
    g = mg.MiniGraph([1,2], [(1, 2)])
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {1: {None: {2: {}}}}
    assert g._edges == {2: {None: {1: {}}}}
    assert g.uedges == {}

    # basic directed with auto-populated nodes
    g = mg.MiniGraph(edges=[(1, 2)])
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {1: {None: {2: {}}}}
    assert g._edges == {2: {None: {1: {}}}}
    assert g.uedges == {}

    # basic with label
    g = mg.MiniGraph([1,2], [(1, 2, 'label')])
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {1: {'label': {2: {}}}}
    assert g._edges == {2: {'label': {1: {}}}}
    assert g.uedges == {}

    # basic with data
    g = mg.MiniGraph([1,2], [(1, 2, None, {'attr': 'val'})])
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {1: {None: {2: {'attr': 'val'}}}}
    assert g._edges == {2: {None: {1: {'attr': 'val'}}}}
    assert g.uedges == {}

    # from here assume g.uedges is {}

    # multiple same source
    g = mg.MiniGraph([1,2,3], [(1, 2), (1, 3)])
    assert g.nodes == {1: {}, 2: {}, 3: {}}
    assert g.edges == {1: {None: {2: {}, 3: {}}}}
    assert g._edges == {2: {None: {1: {}}}, 3: {None: {1: {}}}}

    # multiple same target
    g = mg.MiniGraph([1,2,3], [(1, 2), (3, 2)])
    assert g.nodes == {1: {}, 2: {}, 3: {}}
    assert g.edges == {1: {None: {2: {}}}, 3: {None: {2: {}}}}
    assert g._edges == {2: {None: {1: {}, 3: {}}}}

    # cycle
    g = mg.MiniGraph([1,2], [(1, 2), (2, 1)])
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {1: {None: {2: {}}}, 2: {None: {1: {}}}}
    assert g._edges == {2: {None: {1: {}}}, 1: {None: {2: {}}}}

    # simple loop
    g = mg.MiniGraph([1], [(1, 1)])
    assert g.nodes == {1: {}}
    assert g.edges == {1: {None: {1: {}}}}
    assert g._edges == {1: {None: {1: {}}}}

    # cannot have same edge with same label (see labeled tests below)
    # with pytest.raises(mg.MiniGraphError):
    #     mg.MiniGraph([1, 2], [(1, 2), (1, 2)])


def test_undirected_init():
    # basic undirected
    g = mg.MiniGraph([1,2], [(1, 2, None, None, False)])
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {}
    assert g._edges == {}
    assert g.uedges == {1: {None: {2: {}}}, 2: {None: {1: {}}}}

    # basic undirected with auto-populated nodes
    g = mg.MiniGraph(edges=[(1, 2, None, None, False)])
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {}
    assert g._edges == {}
    assert g.uedges == {1: {None: {2: {}}}, 2: {None: {1: {}}}}

    # basic with label
    g = mg.MiniGraph([1,2], [(1, 2, 'label', None, False)])
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {}
    assert g._edges == {}
    assert g.uedges == {1: {'label': {2: {}}}, 2: {'label': {1: {}}}}

    # basic with data
    g = mg.MiniGraph([1,2], [(1, 2, None, {'attr': 'val'}, False)])
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {}
    assert g._edges == {}
    assert g.uedges == {1: {None: {2: {'attr': 'val'}}},
                        2: {None: {1: {'attr': 'val'}}}}

    # from here assume g.edges and g._edges are both {}

    # multiple same source
    g = mg.MiniGraph(
        [1,2,3],
        [(1, 2, None, None, False), (1, 3, None, None, False)]
    )
    assert g.nodes == {1: {}, 2: {}, 3: {}}
    assert g.uedges == {
        1: {None: {2: {}, 3: {}}},
        2: {None: {1: {}}},
        3: {None: {1: {}}}
    }

    # multiple same target
    g = mg.MiniGraph(
        [1,2,3],
        [(1, 2, None, None, False), (3, 2, None, None, False)]
    )
    assert g.nodes == {1: {}, 2: {}, 3: {}}
    assert g.uedges == {
        1: {None: {2: {}}},
        2: {None: {1: {}, 3: {}}},
        3: {None: {2: {}}}
    }

    # cycle in args raises error
    # with pytest.raises(mg.MiniGraphError):
    #     mg.MiniGraph(
    #         [1,2],
    #         [(1, 2, None, None, False), (2, 1, None, None, False)]
    #     )

    # simple loops are ok
    g = mg.MiniGraph([1], [(1, 1, None, None, False)])
    assert g.uedges == {1: {None: {1: {}}}}

    # cannot have same edge with same label (see labeled tests below)
    # with pytest.raises(mg.MiniGraphError):
    #     mg.MiniGraph(
    #         [1, 2],
    #         [(1, 2, None, None, False), (1, 2, None, None, False)]
    #     )

def test_add_node():
    g = mg.MiniGraph()
    assert g.nodes == {}
    g.add_node(1)
    assert g.nodes == {1: {}}
    # with pytest.raises(mg.MiniGraphError):
    #     g.add_node(1)
    g.add_node(2, data={'attr': 'val'})
    assert g.nodes == {1: {}, 2: {'attr': 'val'}}

def test_remove_node():
    g = mg.MiniGraph(edges=[(1,2), (2,3), (3,1), (1,1)])
    assert g.nodes == {1: {}, 2: {}, 3: {}}
    g.remove_node(1)
    assert g.nodes == {2: {}, 3: {}}
    assert g.edges == {2: {None: {3: {}}}}
    assert g._edges == {3: {None: {2: {}}}}
    with pytest.raises(KeyError):
        g.remove_node(1)

def test_add_edge():
    g = mg.MiniGraph()
    assert g.edges == {}
    g.add_edge(1, 2)
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {1: {None: {2: {}}}}
    assert g._edges == {2: {None: {1: {}}}}
    assert g.uedges == {}
    # with pytest.raises(mg.MiniGraphError):
    #     g.add_edge(1, 2)
    g.add_edge(1, 2, label='label')
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {1: {None: {2: {}}, 'label': {2: {}}}}
    assert g._edges == {2: {None: {1: {}}, 'label': {1: {}}}}
    assert g.uedges == {}
    g = mg.MiniGraph()
    g.add_edge(1, 2, data={'attr': 'val'})
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {1: {None: {2: {'attr': 'val'}}}}
    assert g._edges == {2: {None: {1: {'attr': 'val'}}}}
    assert g.uedges == {}
    g = mg.MiniGraph()
    g.add_edge(1, 2, directed=False)
    assert g.nodes == {1: {}, 2: {}}
    assert g.edges == {}
    assert g._edges == {}
    assert g.uedges == {1: {None: {2: {}}}, 2: {None: {1: {}}}}
    g = mg.MiniGraph()
    g.add_edge(1, 1)
    assert g.nodes == {1: {}}
    assert g.edges == {1: {None: {1: {}}}}
    assert g._edges == {1: {None: {1: {}}}}
    assert g.uedges == {}

def test_remove_edge():
    g = mg.MiniGraph(edges=[(1,2), (2,1)])
    assert g.edges == {1: {None: {2: {}}}, 2: {None: {1: {}}}}
    assert g._edges == {2: {None: {1: {}}}, 1: {None: {2: {}}}}
    with pytest.raises(KeyError):
        g.remove_edge(1, 4)
    assert g.edges == {1: {None: {2: {}}}, 2: {None: {1: {}}}}
    g.remove_edge(1, 2)
    assert g.edges == {2: {None: {1: {}}}}
    assert g._edges == {1: {None: {2: {}}}}
    with pytest.raises(KeyError):
        g.remove_edge(1, 2)

    g = mg.MiniGraph(edges=[(1,1), (1,1,'other')])
    assert g.edges == {1: {None: {1: {}}, 'other': {1: {}}}}
    assert g._edges == {1: {None: {1: {}}, 'other': {1: {}}}}
    g.remove_edge(1, 1)
    assert g.edges == {1: {'other': {1: {}}}}
    assert g._edges == {1: {'other': {1: {}}}}
    g = mg.MiniGraph(edges=[(1,1), (1,1,'other')])
    g.remove_edge(1, 1, label='other')
    assert g.edges == {1: {None: {1: {}}}}
    assert g._edges == {1: {None: {1: {}}}}

    g = mg.MiniGraph(edges=[(1,1), (1,1,None,None,False)])
    assert g.edges == {1: {None: {1: {}}}}
    assert g._edges == {1: {None: {1: {}}}}
    assert g.uedges == {1: {None: {1: {}}}}
    g.remove_edge(1, 1)
    assert g.edges == {}
    assert g._edges == {}
    assert g.uedges == {1: {None: {1: {}}}}
    g = mg.MiniGraph(edges=[(1,1), (1,1,None,None,False)])
    g.remove_edge(1, 1, directed=False)
    assert g.edges == {1: {None: {1: {}}}}
    assert g._edges == {1: {None: {1: {}}}}
    assert g.uedges == {}

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
    assert g.in_degree(1) == 1
    assert g.in_degree(2) == 1
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
    assert g.degree(1) == 1

def test_subgraph():
    with pytest.raises(KeyError):
        mg.MiniGraph([1]).subgraph([2])

    sg = mg.MiniGraph().subgraph([])
    assert len(sg.nodes) == 0
    assert len(sg.edges) == 0
    assert len(sg._edges) == 0
    assert len(sg.uedges) == 0

    sg = mg.MiniGraph([1]).subgraph([])
    assert len(sg.nodes) == 0
    assert len(sg.edges) == 0
    assert len(sg._edges) == 0
    assert len(sg.uedges) == 0

    sg = mg.MiniGraph([1]).subgraph([1])
    assert len(sg.nodes) == 1
    assert len(sg.edges) == 0
    assert len(sg._edges) == 0
    assert len(sg.uedges) == 0

    g = mg.MiniGraph(edges=[(1,2),(2,3),(3,1)])
    sg = g.subgraph([1,2])
    assert sg.nodes == {1: {}, 2: {}}
    assert sg.edges == {1: {None: {2: {}}}}
    assert sg._edges == {2: {None: {1: {}}}}
    assert len(sg.uedges) == 0

    sg = g.subgraph([1,3])
    assert sg.nodes == {1: {}, 3: {}}
    assert sg.edges == {3: {None: {1: {}}}}
    assert sg._edges == {1: {None: {3: {}}}}
    assert len(sg.uedges) == 0

    g = mg.MiniGraph(edges=[(1,1),(1,1,None,None,False)])
    sg = g.subgraph([1])
    assert sg.nodes == {1: {}}
    assert sg.edges == {1: {None: {1: {}}}}
    assert sg._edges == {1: {None: {1: {}}}}
    assert sg.uedges == {1: {None: {1: {}}}}

