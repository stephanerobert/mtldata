import asyncio
import unittest

from flexmock import flexmock
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
        self.datastore.should_receive("get_summary_tree").and_return(
            {'arrond1': [{'essence1': {'tree': 'definition'}}, {'essence2': {'tree': 'definition'}}]})

        response = asyncio.get_event_loop().run_until_complete(self.app.test_client().get("/v1/trees"))
        result = asyncio.get_event_loop().run_until_complete(response.json)

        self.assertEqual(result,
                         {'arrond1': [{'essence1': {'tree': 'definition'}}, {'essence2': {'tree': 'definition'}}]})

    def test_arbres_arrondissement_endpoint(self):
        self.datastore.should_receive("get_trees_arrondissement").and_return(
            {'Trees': "The Trees in the city"})

        response = asyncio.get_event_loop().run_until_complete(self.app.test_client().get("/v1/cities/ville-marie/trees"))
        result = asyncio.get_event_loop().run_until_complete(response.json)

        self.assertEqual(result, {'Trees': "The Trees in the city"})

    def test_arbres_arrondissement_essence_endpoint(self):
        self.datastore.should_receive("get_trees_arrondissement_essence").and_return(
            {'Trees': "The Trees in the city by species"})

        response = asyncio.get_event_loop().run_until_complete(
            self.app.test_client().get("/v1/cities/ville-marie/trees/erable"))
        result = asyncio.get_event_loop().run_until_complete(response.json)

        self.assertEqual(result, {'Trees': "The Trees in the city by species"})

    def test_arrondissements_endpoint(self):
        self.datastore.should_receive("get_arrondissements").and_return({'Trees': "The cities"})

        response = asyncio.get_event_loop().run_until_complete(self.app.test_client().get("/v1/cities"))
        result = asyncio.get_event_loop().run_until_complete(response.json)

        self.assertEqual(result, {'Trees': "The cities"})

    def test_essence_endpoint(self):
        self.datastore.should_receive("get_essences").and_return({'Trees': "The species"})

        response = asyncio.get_event_loop().run_until_complete(self.app.test_client().get("/v1/species"))
        result = asyncio.get_event_loop().run_until_complete(response.json)

        self.assertEqual(result, {'Trees': "The species"})
