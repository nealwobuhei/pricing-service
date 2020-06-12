from flask import Blueprint

learning_blueprint = Blueprint('learning', __name__)


@learning_blueprint.route('/<string:name>')  # only define in the blueprint
def home(name):
    return f"hello, {name}!"


