import requests
from hamcrest import assert_that, is_
from mockserver_friendly import request, response

from test.integration import ServerMockingTestBase
from test.integration.mtl_trees_fixture import mtl_trees


class MtlDataTest(ServerMockingTestBase):

    def setUp(self):
        super().setUp()

    def test_return_agile_devices_with_rbac_token(self):
        self.mock_server.stub(
            request(
                path="/dataset/3e3efad6-9f2f-4cc0-8f1b-92de1ccdb282/resource/c6c5afe8-10be-4539-8eae-93918ea9866e/download/arbres-publics.csv"),
            response(code=200, body=mtl_trees)
        )

        result = requests.get("http://0.0.0.0:8084/v1/arbres")
        result = result.json()

        print(result)

        assert_that(len(result), is_(1))
        assert_that(len(result['Ahuntsic - Cartierville']), is_(8))
        assert_that(result['Ahuntsic - Cartierville'][0], is_('Fevier Skyline'))
        assert_that(result['Ahuntsic - Cartierville'][1], is_('Chicot du Canada'))
        assert_that(result['Ahuntsic - Cartierville'][2], is_('Frene noir Fall Gold'))
        assert_that(result['Ahuntsic - Cartierville'][3], is_('Chene rouge'))
        assert_that(result['Ahuntsic - Cartierville'][4], is_('Chene a gros fruits'))
