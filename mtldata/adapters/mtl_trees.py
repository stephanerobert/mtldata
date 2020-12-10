import asyncio
import csv
from urllib import request

from mtldata.core.objects.objects import Tree


class MtlTrees:
    def __init__(self, url):
        self.url = url

    @asyncio.coroutine
    def get_trees(self):
        filename, headers = request.urlretrieve(self.url)

        with open(filename) as csvfile:
            trees = csv.DictReader(csvfile, delimiter=',')

            for tree in trees:
                yield Tree(essence=tree.pop('Essence_fr'),
                           arrondissement=tree.pop('ARROND_NOM'),
                           longitude=tree.pop('Longitude'),
                           latitude=tree.pop('Latitude'),
                           **tree)
