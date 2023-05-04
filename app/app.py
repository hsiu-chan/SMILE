from flask import Flask
from api.func1 import func1_blueprint
from api.img import img_blueprint

from website import website_blueprint
#from flask_mail import Mail, Message




def create_app():#Application Factories
    app = Flask(__name__, static_url_path='/static/', 
            static_folder='static/')
    app.register_blueprint(website_blueprint)
    app.register_blueprint(img_blueprint)
    app.register_blueprint(func1_blueprint)

    
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = ''
    app.config['MAIL_PASSWORD'] = ''
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    #mail= Mail(app)
    
    return app
