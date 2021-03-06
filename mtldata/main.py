import os

from redis import Redis
from quart import Quart
from quart_cors import cors

from mtldata.adapters.mtl_trees import MtlTrees
from mtldata.api import healthcheck, endpoints
from mtldata.config import load
from mtldata.adapters.storage.sqlite import SQLite
from mtldata.adapters.storage.memory import Memory
from mtldata.core.tree_data import TreeData

config = load(os.environ.get('ENVIRONMENT', 'local'))

mtl_data_adaptor = MtlTrees(config.mtl.tree_url+config.mtl.tree_path)
# datastore = SQLite()
datastore = Memory()

app = Quart(__name__)
app = cors(app, allow_origin="*")

app.config["storage"] = datastore
app.config["cache"] = Redis(config.redis.url)

app.register_blueprint(healthcheck.app)
app.register_blueprint(endpoints.app, url_prefix="/v1")

TreeData.populate_tree_data(mtl_data_adaptor, datastore)
# asyncio.run(TreeData.populate_tree_data(mtl_data_adaptor, datastore))


@app.route('/count', methods=['GET'])
async def arrondissement():
    return str(datastore._count_trees())


if __name__ == '__main__':
    app.run()
