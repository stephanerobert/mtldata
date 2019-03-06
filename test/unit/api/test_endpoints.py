import unittest

from flexmock import flexmock
import asyncio
from quart import Quart

from mtldata.api import endpoints


class TestEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = Quart(__name__)

        self.datastore = flexmock()
        self.app.config["storage"] = self.datastore
        self.app.config["cache"] = flexmock()

        self.app.register_blueprint(endpoints.app, url_prefix="/v1")

    def test_arbres_endpoint(self):
        self.datastore.should_receive("get_summary_tree").and_return({'Trees': "The Trees"})

        response = asyncio.get_event_loop().run_until_complete(self.app.test_client().get("/v1/arbres"))
        result = asyncio.get_event_loop().run_until_complete(response.json)

        self.assertEqual(result, {'Trees': "The Trees"})

    def test_arbres_arrondissement_endpoint(self):
        self.datastore.should_receive("get_trees_arrondissement").and_return(
            {'Trees': "The Trees in the arrondissement"})

        response = asyncio.get_event_loop().run_until_complete(self.app.test_client().get("/v1/arbres/ville-marie"))
        result = asyncio.get_event_loop().run_until_complete(response.json)

        self.assertEqual(result, {'Trees': "The Trees in the arrondissement"})

    def test_arbres_arrondissement_essence_endpoint(self):
        self.datastore.should_receive("get_trees_arrondissement_essence").and_return(
            {'Trees': "The Trees in the arrondissement by essence"})

        response = asyncio.get_event_loop().run_until_complete(
            self.app.test_client().get("/v1/arbres/ville-marie/erable"))
        result = asyncio.get_event_loop().run_until_complete(response.json)

        self.assertEqual(result, {'Trees': "The Trees in the arrondissement by essence"})

    def test_arrondissements_endpoint(self):
        self.datastore.should_receive("get_arrondissements").and_return({'Trees': "The arrondissements"})

        response = asyncio.get_event_loop().run_until_complete(self.app.test_client().get("/v1/arrondissements"))
        result = asyncio.get_event_loop().run_until_complete(response.json)

        self.assertEqual(result, {'Trees': "The arrondissements"})

    def test_essence_endpoint(self):
        self.datastore.should_receive("get_essences").and_return({'Trees': "The essences"})

        response = asyncio.get_event_loop().run_until_complete(self.app.test_client().get("/v1/essences"))
        result = asyncio.get_event_loop().run_until_complete(response.json)

        self.assertEqual(result, {'Trees': "The essences"})
