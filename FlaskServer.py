import json

import Dictionary
import TTMLParser
import main
from flask import (Flask,request,jsonify,send_file,make_response,abort)
import io
import xmltodict
import xml.etree.ElementTree as ET

from Dictionaries import Dictionaries

app = Flask(__name__)
number =0
@app.route("/pose",methods = ["GET"])
def get_pose():
    data  = request.get_data()
    with open('data.xml', 'wb') as f:
        f.write(data)
    subsarray, suffix, language = TTMLParser.getArrfromCaptions("data.xml")
    dict = dictionaries.getdictionarybysuffix(suffix)
    main.create_pose_for_video(dict,subsarray, suffix, language)
    try:
        with open("po.pose", 'rb') as bites:
            return send_file(
                io.BytesIO(bites.read()),
                attachment_filename='hey.pose',
                mimetype='binary'
            )
    except FileNotFoundError:
        abort(404)



dictionaries = main.create_languages_to_suffix_dictionary()
dictionaries.createAllWordToID()
print("loaded index file and all dictionaries")








app.run(port = 5000, threaded = True)