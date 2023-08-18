from flask import Flask
from api.func1 import func1_blueprint
#from api.img import img_blueprint
from api.GetLabelData import GetLabelData_blueprint#取得標注資料
from website import website_home_blueprint,website_pages_blueprint
#from flask_mail import Mail, Message




def create_app():#Application Factories
    app = Flask(__name__, static_url_path='/static/', 
            static_folder='static/')
    app.register_blueprint(website_home_blueprint)
    app.register_blueprint(website_pages_blueprint)

    ###API###
    #app.register_blueprint(img_blueprint)
    app.register_blueprint(func1_blueprint)
    app.register_blueprint(GetLabelData_blueprint)#取得標注資料
    
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = ''
    app.config['MAIL_PASSWORD'] = ''
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    #mail= Mail(app)
    
    return app
