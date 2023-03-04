from ckan.lib.helpers import redirect_to
from ckan.plugins.toolkit import config
from flask import Blueprint


blueprint = Blueprint('desq', __name__)


def redirect_home():
    # Note: redirect_to() preserves the active language, unlike flask.redirect().
    return redirect_to('dataset.search')


blueprint.add_url_rule('/', view_func=redirect_home)
