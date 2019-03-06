from mtldata.model.sqlite import SQLite


class TreeData:
    @staticmethod
    async def populate_tree_data(mtl_data_adaptor, datastore: SQLite):
        for tree in mtl_data_adaptor.get_trees():
            datastore.store_info(tree)
