from flask import Flask, request, Blueprint,jsonify,current_app
from lib.Base64Converter import url_to_img,path_to_base64
from lib.SMILE import SMILE
import uuid
import numpy as np
from os import listdir,path

#from flask_mail import Mail, Message

GetLabelData_blueprint= Blueprint('GetLabelData_blueprint', __name__)

@GetLabelData_blueprint.route('/get_label_data', methods=['POST','GET'])
def upload_img():
    if request.method== 'POST':
        pass
    elif request.method== 'GET':
        return get()

    


def add(data):
    #img_src=str(data.get('image'))
    img,ext=url_to_img(data.get('image'))
    id=uuid.uuid4()
    #filename = "upload_fig/{}.{}".format(id, ext)
    filename = "{}.{}".format('input', ext)

    with open(filename, "wb") as f:
        f.write(img)
    
    nowfig=SMILE(filename,'output' )
    #nowfig.set_predictor()
    nowfig.find_all_tooth()
    #mask,sc=nowfig.predict([[50,14]])

    return {'msg': 'success','filename':filename,"result":nowfig.base64, "score":100}


def get():
    print(path.dirname(path.abspath(__file__)))
    dir_path=f"C:/gits/SMILE/app/TrainData/mask/"
    files = listdir(dir_path)
    for f in files:
        if f.split('.')[-1]=="png":
            return {"fig":path_to_base64(f'{dir_path}{f}')}
    """except:
        return {'msg':'超出範圍'}"""
