import numpy as np
from rdkit.Chem import MolFromSmiles, MolToSmiles, Draw, GetAdjacencyMatrix

from glyles.glycans.monomer import Monomer


# TODO: Extract structure generation and annotation into script and save a file for each structure
# reduce time for preprocessing


class RDKitMonomer(Monomer):
    def __init__(self, origin=None, **kwargs):
        super(RDKitMonomer, self).__init__(origin, **kwargs)
        self.adjacency = None
        self.ringinfo = None
        self.x = None
        self.__get_structure()

    def get_dummy_atoms(self):
        return [34, 52, 84], ["Se", "Te", "Po"]

    def root_atom_id(self, binding_c_id):
        return self.__find_oxygen(binding_c_id)

    def mark(self, position, atom):
        idx = self.__find_oxygen(position)
        self.__get_structure().GetAtomWithIdx(idx).SetAtomicNum(atom)
        self.x[idx, 0] = atom

    def to_smiles(self, root, ring_index):
        smiles = MolToSmiles(self.__get_structure(), rootedAtAtom=root)
        return "".join([(str(int(c) + ring_index) if c.isdigit() else c) for c in smiles])

    def __get_structure(self):
        if self._structure is None:
            self._structure = MolFromSmiles(self._smiles)

            self.adjacency = GetAdjacencyMatrix(self._structure)
            self.ringinfo = self._structure.GetRingInfo().AtomRings()
            self.x = np.zeros((self.adjacency.shape[0], 3))

            # TODO: Find a way to properly define which orientation the ring has!
            mainring = list(reversed(list(self.ringinfo[0]) + list(self.ringinfo[0])))

            for i in range(self.adjacency.shape[0]):
                atom = self._structure.GetAtomWithIdx(i)
                self.x[i, 0] = atom.GetAtomicNum()
                for r in range(len(self.ringinfo)):
                    if i in self.ringinfo[r]:
                        self.x[i, 2] = r + 1
                if self.x[i, 2] == 1 and self.x[i, 0] == 8:
                    self.x[i, 1] = 10

            # TODO: This only works if the C1 atom is part of the ring! (i.e. not for fructose)
            o_index = mainring.index(np.argwhere((self.x[:, 0] == 8) & (self.x[:, 2] == 1)))
            for r in self.ringinfo[0]:
                if self.x[r, 0] != 8:
                    self.x[r, 1] = mainring.index(r, o_index) - o_index

            highest_index = np.max(self.x[:, 1][np.argwhere(self.x[:, 0] == 6)])
            remaining_cs = np.argwhere((self.x[:, 0] == 6) & (self.x[:, 2] == 0))[0]
            for rc in remaining_cs:
                highest_index += 1
                self.x[rc, 1] = highest_index

        return self._structure

    def test(self):
        Draw.MolToImage(self.__get_structure()).save(open("./mol.png", "wb"))

    def __find_oxygen(self, binding_c_id):
        position = np.argwhere(self.x[:, 1] == binding_c_id).squeeze()
        candidates = np.argwhere((self.adjacency[position, :] == 1) & (self.x[:, 0] == 8) & (self.x[:, 2] != 1)).squeeze()
        return int(candidates)

    @staticmethod
    def from_string(mono):
        return RDKitMonomer(origin=Monomer.from_string(mono))
