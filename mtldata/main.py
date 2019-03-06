import asyncio
import os

from redis import Redis
from quart import Quart

from mtldata.adapters.mtl_trees import MtlTrees
from mtldata.api import healthcheck, endpoints
from mtldata.config import load
from mtldata.model.sqlite import SQLite

from mtldata.model.tree_data import TreeData

config = load(os.environ.get('ENVIRONMENT', 'local'))

mtl_data_adaptor = MtlTrees(config.mtl.tree_url+config.mtl.tree_path)
datastore = SQLite()

app = Quart(__name__)

app.config["storage"] = datastore
app.config["cache"] = Redis(config.redis.url)

app.register_blueprint(healthcheck.app)
app.register_blueprint(endpoints.app, url_prefix="/v1")

# Thread(target=TreeData.populate_tree_data, args=(mtl_data_adaptor, datastore))
asyncio.run(TreeData.populate_tree_data(mtl_data_adaptor, datastore))


@app.route('/count', methods=['GET'])
async def arrondissement():
    return str(datastore._count_trees())


if __name__ == '__main__':
    app.run()
