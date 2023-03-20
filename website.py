from flask import Blueprint,render_template


website_blueprint = Blueprint('website_blueprint', __name__)

@website_blueprint.route('/')
def home():
    return render_template("index.html")
