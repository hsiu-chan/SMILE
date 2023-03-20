from flask import Flask, request, Blueprint,jsonify,current_app
import base64
import re
import uuid



#from flask_mail import Mail, Message

img_blueprint = Blueprint('img_blueprint', __name__)

@img_blueprint.route('/upload_img', methods=['POST'])
def upload_img():
    data=request.get_json()
    img_src=str(data.get('image'))
    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", img_src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        img = result.groupdict().get("data")
        img=base64.b64decode(img)
        filename = "upload_fig/{}.{}".format(uuid.uuid4(), ext)
        with open(filename, "wb") as f:
            f.write(img)

    #return json.JSONEncoder.default({'validate': 'formula success'})
    return {'validate': 'success'}
