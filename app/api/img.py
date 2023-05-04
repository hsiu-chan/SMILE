from flask import Flask, request, Blueprint,jsonify,current_app
from lib.Base64 import url_to_img,path_to_base64
from lib.SMILE import SMILE, SMILE_0
import uuid


#from flask_mail import Mail, Message

img_blueprint = Blueprint('img_blueprint', __name__)

@img_blueprint.route('/upload_img', methods=['POST'])
def upload_img():
    data=request.get_json()
    #img_src=str(data.get('image'))
    img,ext=url_to_img(data.get('image'))
    id=uuid.uuid4()
    #filename = "upload_fig/{}.{}".format(id, ext)
    filename = "{}.{}".format('input', ext)

    with open(filename, "wb") as f:
        f.write(img)
    
    nowfig=SMILE(filename,'output' )
    nowfig.find_mouse()
    #nowfig.set_predictor()
    #mask,sc=nowfig.predict([[50,14]])

    return {'msg': 'success','filename':filename,"result":nowfig.base64, "score":100}

"""@img_blueprint.route('/download_img', methods=['GET'])
def download_img():
    filename=request.get_json().get('filename')
    img_path=f'upload_fig/{filename}'
    base64_img = path_to_base64(img_path)  # base64编码
    return {'msg':'success',"base64_img":img_to_base64(img)}"""
