import abc


class Storage(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def store_info(self, tree):
        pass

    @abc.abstractmethod
    def get_summary_tree(self):
        pass

    @abc.abstractmethod
    def get_trees_arrondissement(self, arrondissement):
        pass

    @abc.abstractmethod
    def get_trees_arrondissement_essence(self, arrondissement, essence):
        pass

    @abc.abstractmethod
    def get_arrondissements(self):
        pass

    @abc.abstractmethod
    def get_essences(self):
        pass

    @abc.abstractmethod
    def get_trees_essences_in_arrondissement(self):
        pass
