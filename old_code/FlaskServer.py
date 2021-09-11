import json
import requests
import Dictionary
import TTMLParser
import VttParser
import SRTParser
import PoseCreator
from urllib.parse import urlparse
from flask import (Flask, request, jsonify, send_file, make_response, abort)
import io
from Dictionaries import Dictionaries
from flask_cors import CORS
import random
import os
import urllib
import youtubeParser

app = Flask(__name__)
CORS(app)


# this server supports:
#   getting a pose for sentence
#   getting a pose for a video


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
    PoseCreator.create_pose_for_video(dict, subsarray, signlang, language, totaltime)
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
    if dict is None:
        return 'bad request, language pair not found', 400
    n = random.randint(0, 2002)
    language = "en"
    filename, sentence_found = PoseCreator.create_pose_for_sentence(dict, sentence, signlang, language, n)
    if sentence_found is None:
        return 'could not find a word', 400
    try:
        with open(filename, 'rb') as bites:
            response = make_response(send_file(
                io.BytesIO(bites.read()),
                attachment_filename=filename,
                mimetype='binary'
            ))
            response.headers["sentence_found"] = sentence_found
            return response
    except FileNotFoundError:
        abort(404)


@app.route("/youtube/", methods=["GET"])
def translateYoutube():
    r = request
    vidId = request.args["v"]
    lang = "en"
    signlang = "en.us"
    text = youtubeParser.get_youtube_subtitles(vidId, lang)
    text = text.decode("utf-8")
    if text == '':
        abort(404)
    subsarray, totaltime = youtubeParser.get_captions(text)
    dict = dictionaries.getdictionarybysuffix(signlang)
    language = signlang[0:2]
    PoseCreator.create_pose_for_video(dict, subsarray, signlang, language, totaltime)
    try:
        with open("po.pose", 'rb') as bites:
            return send_file(
                io.BytesIO(bites.read()),
                attachment_filename='hey.pose',
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


dictionaries = Dictionaries()
dictionaries.createAllWordToID()
for dic in dictionaries.dictionaries:
    dic.dict_array = Dictionary.create_length_Array(dic.wordToID)
print("loaded index file and all dictionaries")
app.run(port=5000, threaded=True)

# data = request.json
# lang = data["language"]
# subtitlesad = (data["url"])
# signlang = (data["signlang"])
