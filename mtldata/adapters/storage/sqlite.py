import json
import sqlite3

from mtldata.core.storage import Storage


class SQLite(Storage):
    def __init__(self):
        self.connection = sqlite3.connect(':memory:')
        self.arrondissements = None
        self.essences = None

        self._create_tables()

    def _create_tables(self):
        self.connection.cursor().execute(
            '''CREATE TABLE trees (essence varchar(255), arrondissement varchar(255), longitude, latitude, other_info varchar(255))''')

    def store_info(self, tree):
        self.connection.cursor().execute(
            "INSERT INTO trees ('essence', 'arrondissement', 'longitude', 'latitude', 'other_info') VALUES (?,?,?,?,?)",
            [tree.essence, tree.arrondissement, tree.longitude, tree.latitude, json.dumps(tree.other_info)])
        self.connection.commit()

    def get_summary_tree(self):
        trees = {}
        if self.arrondissements is None:
            self._fetch_arrondissements()

        for arrondissement in self.arrondissements:
            print(arrondissement)
            data = self.connection.cursor().execute("SELECT DISTINCT essence FROM trees where arrondissement=?",
                                       [arrondissement]).fetchall()
            trees[arrondissement] = [tree[0] for tree in data]

        return trees

    def get_trees(self):
        trees = {}
        if self.arrondissements is None:
            self._fetch_arrondissements()

        for arrondissement in self.arrondissements:
            arrond = self.get_trees_arrondissement(arrondissement)

            if arrond:
                trees[arrondissement] = arrond

        return trees

    def get_trees_arrondissement(self, arrondissement):
        arrond = {}
        if self.essences is None:
            self._fetch_essences()

        for essence in self.essences:
            trees = self.get_trees_arrondissement_essence(arrondissement, essence)
            if trees:
                arrond[essence] = trees

        return arrond

    def get_trees_arrondissement_essence(self, arrondissement, essence):
        trees = []
        data = self.connection.cursor().execute(
            "SELECT essence, arrondissement, longitude, latitude, other_info FROM trees WHERE arrondissement = ? and essence = ?",
            [arrondissement, essence]).fetchall()

        if data:
            for tree in data:
                trees.append(dict(longitude=tree[2], latitude=tree[3], **json.loads(tree[4])))

        return trees

    def get_arrondissements(self):
        if self.arrondissements is None:
            self._fetch_arrondissements()
        return self.arrondissements

    def get_essences(self):
        if self.essences is None:
            self._fetch_essences()
        return self.essences

    def _fetch_arrondissements(self):
        self.arrondissements = []
        arrondissements = self.connection.cursor().execute("SELECT DISTINCT arrondissement FROM trees")
        for arrondissement in arrondissements.fetchall():
            self.arrondissements.append(arrondissement[0])

    def _fetch_essences(self):
        self.essences = []
        essences = self.connection.cursor().execute("SELECT DISTINCT essence FROM trees")
        for essence in essences.fetchall():
            self.essences.append(essence[0])

    def _count_trees(self):
        return self.connection.cursor().execute("SELECT COUNT(essence) FROM trees").fetchone()
