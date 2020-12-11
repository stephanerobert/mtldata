from mtldata.core.storage import Storage


class TreeData:
    @staticmethod
    def populate_tree_data(mtl_data_adaptor, datastore: Storage):
        for tree in mtl_data_adaptor.get_trees():
            datastore.store_info(tree)
