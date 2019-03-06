from quart import Blueprint

app = Blueprint('healthcheck', __name__)

app._message = None


@app.route("/healthcheck")
async def hello():
    return 'hello'
