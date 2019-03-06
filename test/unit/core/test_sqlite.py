import unittest

from flexmock import flexmock
from hamcrest import assert_that, is_

from mtldata.model.objects import Tree
from mtldata.model.sqlite import SQLite


class TestSQLite(unittest.TestCase):
    def setUp(self):
        self.sqlite = SQLite()
        self.sqlite.cursor = flexmock()

        self.tree = Tree('erable', 'ville-marie', '-73.715515', '45.535151', a='1', b='2')

    def test_store_info(self):
        self.sqlite.cursor.should_receive('execute').with_args(
            "INSERT INTO trees ('essence', 'arrondissement', 'longitude', 'latitude', 'other_info') VALUES (?,?,?,?,?)",
            ['erable', 'ville-marie', '-73.715515', '45.535151', '{"a": "1", "b": "2"}']).once()
        self.sqlite.store_info(self.tree)

    def test_get_trees(self):
        self.sqlite.arrondissements = ['ville-marie', 'rosemont']
        self.sqlite.essences = ['erable', 'bouleau']
        data1 = flexmock()
        data1.should_receive('fetchall').once().and_return((['ville-marie', 'erable', '1', '2', '{"a":1}'],))
        data2 = flexmock()
        data2.should_receive('fetchall').once().and_return((['ville-marie', 'bouleau', '3', '4', '{"a":1}'],))
        data3 = flexmock()
        data3.should_receive('fetchall').once().and_return((['rosemont', 'erable', '5', '6', '{"a":1}'],))
        data4 = flexmock()
        data4.should_receive('fetchall').once().and_return((['rosemont-marie', 'bouleau', '7', '8', '{"a":1}'],))

        self.sqlite.cursor.should_receive('execute') \
            .with_args(
            "SELECT essence, arrondissement, longitude, latitude, other_info FROM trees WHERE arrondissement = ? and essence = ?",
            ['ville-marie', 'erable']) \
            .once() \
            .and_return(data1)
        self.sqlite.cursor.should_receive('execute') \
            .with_args(
            "SELECT essence, arrondissement, longitude, latitude, other_info FROM trees WHERE arrondissement = ? and essence = ?",
            ['ville-marie', 'bouleau']) \
            .once() \
            .and_return(data2)
        self.sqlite.cursor.should_receive('execute') \
            .with_args(
            "SELECT essence, arrondissement, longitude, latitude, other_info FROM trees WHERE arrondissement = ? and essence = ?",
            ['rosemont', 'erable']) \
            .once() \
            .and_return(data3)
        self.sqlite.cursor.should_receive('execute') \
            .with_args(
            "SELECT essence, arrondissement, longitude, latitude, other_info FROM trees WHERE arrondissement = ? and essence = ?",
            ['rosemont', 'bouleau']) \
            .once() \
            .and_return(data4)

        trees = self.sqlite.get_trees()

        assert_that(trees['ville-marie'], is_({'erable': [{'longitude': '1', 'latitude': '2', 'a': 1}],
                                               'bouleau': [{'longitude': '3', 'latitude': '4', 'a': 1}]}))
        assert_that(trees['rosemont'], is_({'erable': [{'longitude': '5', 'latitude': '6', 'a': 1}],
                                            'bouleau': [{'longitude': '7', 'latitude': '8', 'a': 1}]}))

    def test_get_arrondissements(self):
        self.sqlite.arrondissements = None
        data = flexmock()
        data.should_receive('fetchall').once().and_return(('ville-marie',), ('rosemont',))
        self.sqlite.cursor.should_receive('execute') \
            .with_args("SELECT DISTINCT arrondissement FROM trees") \
            .once() \
            .and_return(data)

        assert_that(self.sqlite.get_arrondissements(), is_(['ville-marie', 'rosemont']))

    def test_get_essences(self):
        self.sqlite.essences = None
        data = flexmock()
        data.should_receive('fetchall').once().and_return(('bouleau',), ('erable',))
        self.sqlite.cursor.should_receive('execute') \
            .with_args("SELECT DISTINCT essence FROM trees") \
            .once() \
            .and_return(data)

        assert_that(self.sqlite.get_essences(), is_(['bouleau', 'erable']))
