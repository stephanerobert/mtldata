import unittest
from unittest.mock import mock_open, patch

from flexmock import flexmock
from hamcrest import assert_that, is_

from mtldata.adapters import mtl_trees

mtl_tree_csv = """INV_TYPE,EMP_NO,ARROND,ARROND_NOM,Rue,COTE,No_civique,Emplacement,Coord_X,Coord_Y,SIGLE,Essence_latin,Essence_fr,ESSENCE_ANG,DHP,Date_releve,Date_plantation,LOCALISATION,CODE_PARC,NOM_PARC,Longitude,Latitude
"H",6,1,"Ahuntsic - Cartierville",,,,"Parterre Gazonné",287967.933,5043937.611,"GLTRSK","Gleditsia triacanthos 'Skyline'","Févier Skyline","Skyline Honey-Locust",25,"2018-06-26T00:00:00","2004-06-10T00:00:00",,"0005-000","RAIMBAULT",-73.715515,45.535151"""


class TestMtlTrees(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data=mtl_tree_csv)
    def test_get_trees(self, _):
        flexmock(mtl_trees.request) \
            .should_receive("urlretrieve") \
            .with_args("http://fake.url") \
            .and_return('filename.csv', None)

        mtltrees = mtl_trees.MtlTrees('http://fake.url')
        trees = mtltrees.get_trees()
        for tree in trees:
            assert_that(tree.arrondissement, is_("Ahuntsic - Cartierville"))
            assert_that(tree.essence, is_("Févier Skyline"))
            assert_that(tree.latitude, is_("45.535151"))
            assert_that(tree.longitude, is_("-73.715515"))
