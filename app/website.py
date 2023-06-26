from flask import Blueprint,render_template,abort
from jinja2 import TemplateNotFound


website_home_blueprint = Blueprint('website_home_blueprint', __name__)

@website_home_blueprint.route('/')
def home():
    return render_template("index.html")

website_pages_blueprint = Blueprint('website_pages_blueprint', __name__)

@website_pages_blueprint.route('/pages/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)
