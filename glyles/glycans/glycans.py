from enum import Enum

import networkx as nx


class Chirality(Enum):
    # relative to haworth notation
    UP = 1
    DOWN = 2
    NONE = 3


class Atom(Enum):
    N = "N"
    C = "C"
    O = "O"
    X = "X"
    Y = "Y"
    Z = "Z"


class Glycan(Enum):
    GLC = {"name": "Glc", "smiles": "C([C@@H]1[C@H]([C@@H]([C@H](C(O1)O)O)O)O)O", "struct": None}
    FRU = {"name": "Fru", "smiles": "C([C@@H]1[C@H]([C@@H](C(O1)(CO)O)O)O)O", "struct": None}
    MAN = {"name": "Man", "smiles": "C([C@@H]1[C@H]([C@@H]([C@@H](C(O1)O)O)O)O)O", "struct": None}
    GAL = {"name": "Gal", "smiles": "C([C@@H]1[C@@H]([C@@H]([C@H](C(O1)O)O)O)O)O", "struct": None}
    TAL = {"name": "Tal", "smiles": "C([C@@H]1[C@@H]([C@@H]([C@@H](C(O1)O)O)O)O)O", "struct": None}

    def structure(self):
        if self.value["struct"] is None:
            # TODO: Implement a parser for SMILES -> smiles.smiles.SMILES.read()
            g = nx.Graph()
            g.add_nodes_from([
                (1, {"type": Atom.C, "chiral": Chirality.NONE, "ring": True}),
                (2, {"type": Atom.C, "chiral": Chirality.NONE, "ring": True}),
                (3, {"type": Atom.C, "chiral": Chirality.NONE, "ring": True}),
                (4, {"type": Atom.C, "chiral": Chirality.NONE, "ring": True}),
                (5, {"type": Atom.C, "chiral": Chirality.NONE, "ring": True}),
                (6, {"type": Atom.C, "chiral": Chirality.NONE, "ring": False}),
                (10, {"type": Atom.O, "chiral": Chirality.NONE, "ring": True}),
                (11, {"type": Atom.O, "chiral": Chirality.NONE, "ring": False}),
                (12, {"type": Atom.O, "chiral": Chirality.NONE, "ring": False}),
                (13, {"type": Atom.O, "chiral": Chirality.NONE, "ring": False}),
                (14, {"type": Atom.O, "chiral": Chirality.NONE, "ring": False}),
                (15, {"type": Atom.O, "chiral": Chirality.NONE, "ring": False}),
            ])
            if self == Glycan.GLC:
                g.add_edges_from([
                    (10, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 10),
                    (1, 11), (2, 12), (3, 13), (4, 14), (5, 6), (6, 15),
                ])
                nx.set_node_attributes(g, {2: {"chiral": Chirality.DOWN}, 3: {"chiral": Chirality.UP},
                                           4: {"chiral": Chirality.DOWN}, 5: {"chiral": Chirality.UP}})
            elif self == Glycan.FRU:
                g.add_edges_from([
                    (10, 2), (2, 3), (3, 4), (4, 5), (5, 10),
                    (1, 2), (1, 11), (2, 12), (3, 13), (4, 14), (5, 6), (6, 15),
                ])
                nx.set_node_attributes(g, {3: {"chiral": Chirality.UP}, 4: {"chiral": Chirality.DOWN},
                                           5: {"chiral": Chirality.UP}})
            elif self == Glycan.MAN:
                g.add_edges_from([
                    (10, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 10),
                    (1, 11), (2, 12), (3, 13), (4, 14), (5, 6), (6, 15)
                ])
                nx.set_node_attributes(g, {2: {"chiral": Chirality.UP}, 3: {"chiral": Chirality.UP},
                                           4: {"chiral": Chirality.DOWN}, 5: {"chiral": Chirality.UP}})
            elif self == Glycan.GAL:
                g.add_edges_from([
                    (10, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 10),
                    (1, 11), (2, 12), (3, 13), (4, 14), (5, 6), (6, 15),
                ])
                nx.set_node_attributes(g, {2: {"chiral": Chirality.DOWN}, 3: {"chiral": Chirality.UP},
                                           4: {"chiral": Chirality.UP}, 5: {"chiral": Chirality.UP}})
            elif self == Glycan.TAL:
                g.add_edges_from([
                    (10, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 10),
                    (1, 11), (2, 12), (3, 13), (4, 14), (5, 6), (6, 15),
                ])
                nx.set_node_attributes(g, {2: {"chiral": Chirality.UP}, 3: {"chiral": Chirality.UP},
                                           4: {"chiral": Chirality.UP}, 5: {"chiral": Chirality.UP}})
            self.value["struct"] = g

        return self.value["struct"]


def from_string(mono):
    """

    Args:
        mono (str):

    Returns:
        Glycan according to the monosaccharide provided via mono
    """
    return Glycan[mono.upper()]


print(Glycan.GLC.structure())
