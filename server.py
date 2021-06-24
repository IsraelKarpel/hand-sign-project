import json
import requests
import Dictionary
import TTMLParser
import VttParser
import SRTParser
import main
from flask import (Flask, request, jsonify, send_file, make_response, abort)
import io
from Dictionaries import Dictionaries
from flask_cors import CORS
import random
import os
import urllib

app = Flask(__name__)
CORS(app)


# this server supports:
#   getting a pose for sentence
#   getting a pose for a video



@app.route("/pose", methods=["GET"])
def get_pose():
    data = request.get_data()
    with open('data.xml', 'wb') as f:
        f.write(data)
    subsarray, suffix, language = TTMLParser.getArrfromCaptions("data.xml")
    dict = dictionaries.getdictionarybysuffix(suffix)
    main.create_pose_for_video(dict, subsarray, suffix, language, 0)
    try:
        with open("po.pose", 'rb') as bites:
            return send_file(
                io.BytesIO(bites.read()),
                attachment_filename='hey.pose',
                mimetype='binary'
            )
    except FileNotFoundError:
        abort(404)


@app.route("/video/", methods=["GET"])
def translate():
    r = request
    url = request.args["path"]
    subtitlesad = url
    signlang = request.args["lang"]
    filename = get_subtitles(subtitlesad)
    if subtitlesad[(len(subtitlesad) - 3):] == 'vtt':
        subsarray, totaltime = VttParser.get_vtt_captions(filename)
    elif subtitlesad[(len(subtitlesad) - 3):] == 'srt':
        subsarray, totaltime = SRTParser.get_srt_captions(filename)
    elif subtitlesad[(len(subtitlesad) - 2):] == 'ml':
        subsarray, totaltime = TTMLParser.get_ttml_captions(filename)
    else:
        return 'Captions file not supported!', 400
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print("The file does not exist")
    dict = dictionaries.getdictionarybysuffix(signlang)
    language = signlang[0:2]
    main.create_pose_for_video(dict, subsarray, signlang, language, totaltime)
    try:
        with open("po.pose", 'rb') as bites:
            return send_file(
                io.BytesIO(bites.read()),
                attachment_filename='hey.pose',
                mimetype='binary'
            )
    except FileNotFoundError:
        abort(404)


@app.route("/sentence/", methods=["GET"])
def translate_sentence():
    r = request
    # sentence = urllib.parse(request.args["sentence"])
    sentence = request.args["sentence"]
    signlang = request.args["lang"]
    sentence = sentence.replace("+", ' ')
    dict = dictionaries.getdictionarybysuffix(signlang)
    n = random.randint(0, 22)
    language = "en"
    filename = main.create_pose_for_sentence(dict, sentence, signlang, language, n)
    try:
        with open(filename, 'rb') as bites:
            return send_file(
                io.BytesIO(bites.read()),
                attachment_filename=filename,
                mimetype='binary'
            )
    except FileNotFoundError:
        abort(404)


def get_subtitles(urlad):
    # sending get request and saving the response as response object
    r = requests.get(url=urlad)
    filename = urlad[10:]
    filename = filename.replace('/', "_")
    filename = filename
    with open(filename, 'wb') as f:
        f.write(r.content)
    return filename


dictionaries = main.create_languages_to_suffix_dictionary()
dictionaries.createAllWordToID()
print("loaded index file and all dictionaries")
app.run(host= "127.0.0.1",port=4001, threaded=True)





# data = request.json
# lang = data["language"]
# subtitlesad = (data["url"])
# signlang = (data["signlang"])