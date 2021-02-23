from functools import wraps
from tempfile import NamedTemporaryFile

from gmplot import gmplot
from quart import Blueprint, jsonify, send_file, request

app = Blueprint('endpoints', __name__)

app.key = None
app.datastore = None
app.cache = None

def sorted_paging(sort_by_default):
    def sorted_paging_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            limit = int(request.args.get('limit', 100))
            offset = int(request.args.get('offset', 0))
            sort_direction = request.args.get('direction', 'ASC')

            payload = {'list': await func(*args, **kwargs)}

            payload['total'] = len(payload['list'])
            payload['list'] = payload['list'][offset:offset + limit]
            payload['limit'] = limit
            payload['offset'] = offset
            payload['sortBy'] = sort_by
            payload['direction'] = sort_direction

            return jsonify(payload)

        return wrapper

    return sorted_paging_decorator


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


@app.route('/essences', methods=['GET'])
async def essences():
    return jsonify(app.datastore.get_essences())


@app.route('/arbres', methods=['GET'])
async def arbres():
    return jsonify(app.datastore.get_summary_tree())


@app.route('/arrondissements', methods=['GET'])
async def arrondissements():
    return jsonify(app.datastore.get_arrondissements())


@app.route('/arrondissements/<arrondissement>/arbres', methods=['GET'])
async def arrondissement(arrondissement):
    return jsonify(app.datastore.get_trees_arrondissement(arrondissement))


@app.route('/arrondissements/<arrondissement>/arbres/essences', methods=['GET'])
async def essences_in_arrondissement(arrondissement):
    return jsonify(app.datastore.get_trees_essences_in_arrondissement(arrondissement))


@app.route('/arrondissements/<arrondissement>/arbres/essences/<essence>', methods=['GET'])
async def essence(arrondissement, essence):
    return jsonify(app.datastore.get_trees_arrondissement_essence(arrondissement, essence))


@app.route('/arrondissements/<arrondissement>/arbres/essences/<essence>/map', methods=['GET'])
async def maps(arrondissement, essence):
    api_key = request.args.get('key', '')
    trees = app.datastore.get_trees_arrondissement_essence(arrondissement, essence)

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
