import json

import Dictionary
import TTMLParser
import PoseCreator
from flask import (Flask,request,jsonify,send_file,make_response,abort)
import io
import xmltodict
import xml.etree.ElementTree as ET

from Dictionaries import Dictionaries

app = Flask(__name__)
number =0
@app.route("/subs",methods = ["GET"])
def get_subs():
    f = open('data.xml', 'r')
    xml = f.read()
    f.close()
    resp = app.make_response(xml)
    resp.mimetype = "text/xml"
    return resp
    # with open('data.xml', 'rb') as bites:
    #     return send_file(
    #         io.BytesIO(bites.read()),
    #         attachment_filename='hey.pose',
    #         mimetype='binary'
    #     )


app.run(port = 5005, threaded = True)