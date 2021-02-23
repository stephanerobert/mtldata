from mtldata.core.storage import Storage


class Memory(Storage):
    def __init__(self):
        self.arbres = {}
        self.count = 0

    def store_info(self, tree):
        self.arbres[tree.arrondissement] = self.arbres.get(tree.arrondissement, {})
        self.arbres[tree.arrondissement][tree.essence] = self.arbres[tree.arrondissement].get(tree.essence, [])
        self.arbres[tree.arrondissement][tree.essence].append(tree.__dict__)

        self.count = self.count + 1

    def get_summary_tree(self):
        trees = {}

        for arrondissement, arbre in self.arbres.items():
            trees[arrondissement] = list(set([essence for essence, info in arbre.items()]))
        return trees

    def get_trees_arrondissement(self, arrondissement):
        return self.arbres.get(arrondissement, [])

    def get_trees_essences_in_arrondissement(self, arrondissement):
        return list(self.arbres[arrondissement].keys())

    def get_trees_arrondissement_essence(self, arrondissement, essence):
        essences = self.arbres[arrondissement].items()
        return [v for e, v in essences if e == essence][0]

    def get_arrondissements(self):
        return list(self.arbres.keys())

    def get_essences(self):
        groupe = []
        for arrondissement, essences in self.arbres.items():
            groupe = groupe + list(essences.keys())
        return list(set(groupe))

    def _count_trees(self):
        return self.count
