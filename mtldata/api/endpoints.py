from functools import wraps
from tempfile import NamedTemporaryFile

from gmplot import gmplot
from quart import Blueprint, jsonify, send_file, request

app = Blueprint('endpoints', __name__)

app.key = None
app.datastore = None
app.cache = None


def cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = '-'.join([func.__name__] + list(args))
        result = app.cache.get(key)

        if result is None:
            result = func(*args, **kwargs)
            app.cache.set(key, result)

        return result

    return wrapper


@app.record
def record_auth(setup_state):
    app.datastore = setup_state.app.config["storage"]
    app.datastore = setup_state.app.config["storage"]
    app.cache = setup_state.app.config["cache"]


@app.route('/species', methods=['GET'])
async def species():
    return jsonify(app.datastore.get_essences())


@app.route('/trees', methods=['GET'])
async def trees():
    return jsonify(app.datastore.get_summary_tree())


@app.route('/cities', methods=['GET'])
async def cities():
    return jsonify(app.datastore.get_arrondissements())


@app.route('/cities/<city>/trees', methods=['GET'])
async def city(city):
    return jsonify(app.datastore.get_trees_arrondissement(city))


@app.route('/cities/<city>/trees/species', methods=['GET'])
async def essences_in_arrondissement(city):
    return jsonify(app.datastore.get_trees_essences_in_arrondissement(city))


@app.route('/cities/<city>/trees/species/<species>', methods=['GET'])
async def species_in_city(city, species):
    return jsonify(app.datastore.get_trees_arrondissement_essence(city, species))


@app.route('/cities/<city>/trees/species/<species>/map', methods=['GET'])
async def maps(city, species):
    api_key = request.args.get('key', '')
    trees = app.datastore.get_trees_arrondissement_essence(city, species)

    gmap = gmplot.GoogleMapPlotter(45.5367554, -73.801757, 11.02, apikey=api_key)
    gmap.write_point = _write_point
    for tree in trees:
        gmap.marker(float(tree['latitude']), float(tree['longitude']), 'green')

    filename = NamedTemporaryFile(suffix='.html', delete=False).name
    gmap.draw(filename)

    return await send_file(filename)


# Monkey patching because, for some reason, the author decided to use local images...
# which are not available to client browsers.
def _write_point(f, lat, lon, color, title):
    f.write('\t\tvar latlng = new google.maps.LatLng(%f, %f);\n' %
            (lat, lon))
    f.write('\t\tvar img = new google.maps.MarkerImage(\'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|{}\');\n'.format(color))
    f.write('\t\tvar marker = new google.maps.Marker({\n')
    f.write('\t\ttitle: "%s",\n' % title)
    f.write('\t\ticon: img,\n')
    f.write('\t\tposition: latlng\n')
    f.write('\t\t});\n')
    f.write('\t\tmarker.setMap(map);\n')
    f.write('\n')
