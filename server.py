import json
import youtubeParser
import requests
import Dictionary
import TTMLParser
import VttParser
import SRTParser
import PoseCreator
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
# getting a pose for a youtube video


@app.route("/pose", methods=["GET"])
def get_pose():
    data = request.get_data()
    with open('data.xml', 'wb') as f:
        f.write(data)
    subsarray, suffix, language = TTMLParser.getArrfromCaptions("data.xml")
    dict = dictionaries.getdictionarybysuffix(suffix)
    PoseCreator.create_pose_for_video(dict, subsarray, suffix, language, 0)
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


# @app.route("/sentence/", methods=["GET"])
# def translate_sentence():
#     # sentence = urllib.parse(request.args["sentence"])
#     sentence = request.args["sentence"]
#     signlang = request.args["lang"]
#     sentence = sentence.replace("+", ' ')
#     dict = dictionaries.getdictionarybysuffix(signlang)
#     if dict is None:
#         return 'bad request, language pair not found', 400
#     n = random.randint(0, 2002)
#     language = signlang[:2]
#     filename,sentence_found = main.create_pose_for_sentence(dict, sentence, signlang, language, n)
#     if sentence_found is None:
#         return 'could not find a word', 400
#     try:
#         with open(filename, 'rb') as bites:
#             response = make_response(send_file(
#                 io.BytesIO(bites.read()),
#                 attachment_filename=filename,
#                 mimetype='binary'
#             ))
#             response.headers["Accepted-sentence"]= sentence_found.encode("utf-8")
#             return response
#     except FileNotFoundError:
#         abort(404)

#
# @app.route("/sentence/", methods=["GET"])
# def translate_sentence_new():
#     # sentence = urllib.parse(request.args["sentence"])
#     # lang = request.args["lang"]
#     # if lang:
#     #     sourcelang = lang
#     #     destlang = lang
#     # else:
#     sourcelang = request.args["slang"] # en
#     destlang = request.args["dlang"] # us
#     sentence = request.args["sentence"]
#     try:
#         fps = int(request.args["fps"])
#     except:
#         fps = 40
#     sentence = sentence.replace("+", ' ')
#     dict = dictionaries.getdictionarybysuffix(sourcelang)
#     if dict is None:
#         return 'bad request, source language pair not found', 400
#     n = random.randint(0, 2002)
#     language = sourcelang[:2]
#
#     if destlang == sourcelang:
#         filename, sentence_found = main.create_pose_for_sentence(dict, sentence, sourcelang, language, n, fps)
#     else:
#         dict_dest = dictionaries.getdictionarybysuffix(destlang)
#         if dict_dest is None:
#             return 'bad request, destination language pair not found', 400
#         filename, sentence_found = main.create_pose_for_sentence_dest_lang(dict, sentence, sourcelang, dict_dest,
#                                                                            language, n, fps)
#     if sentence_found is None:
#         return 'could not find a word', 400
#     try:
#         with open(filename, 'rb') as bites:
#             response = make_response(send_file(
#                 io.BytesIO(bites.read()),
#                 attachment_filename=filename,
#                 mimetype='binary'
#             ))
#             response.headers["Accepted-sentence"] = sentence_found.encode("utf-8")
#             return response
#     except FileNotFoundError:
#         abort(404)

# new
@app.route("/sentence/", methods=["GET"])
def translate_sentence_new():
    # sentence = urllib.parse(request.args["sentence"])
    # lang = request.args["lang"]
    # if lang:
    #     sourcelang = lang
    #     destlang = lang
    # else:
    sourcelang = request.args["slang"]  # en
    destlang = request.args["dlang"]  # us
    sentence = request.args["sentence"]
    try:
        fps = int(request.args["fps"])
    except:
        fps = 40
    sentence = sentence.replace("+", ' ')
    n = random.randint(0, 2002)
    dictoptimum = dictionaries.getdictionarybysuffix(sourcelang + '.' + destlang)
    if dictoptimum:
        filename, sentence_found = PoseCreator.create_pose_for_sentence(dictoptimum, sentence, (sourcelang + '.' + destlang),
                                                                        sourcelang, n, fps)
    else:
        dicts = dictionaries.get_dictionaries_by_lang(sourcelang)
        if dicts is None:
            return 'bad request, source language pair not found', 400
        else:
            dict_dest = dictionaries.getdictionarybysuffix2(destlang)
            if dict_dest is None:
                return 'bad request, destination language pair not found', 400
            filename, sentence_found = PoseCreator.create_pose_for_sentence_dest_lang(dicts, sentence, sourcelang, dict_dest,
                                                                                      sourcelang, n, fps)
    if sentence_found is None:
        return 'could not find a word', 400
    try:
        with open(filename, 'rb') as bites:
            response = make_response(send_file(
                io.BytesIO(bites.read()),
                attachment_filename=filename,
                mimetype='binary'
            ))
            response.headers["Accepted-sentence"] = sentence_found.encode("utf-8")
            return response
    except FileNotFoundError:
        abort(404)


@app.route("/youtube/", methods=["GET"])
def translateYoutube():
    r = request
    vidId = request.args["v"]
    signlang = request.args["lang"]
    lang = request.args["lang"][:2]
    text = youtubeParser.get_youtube_subtitles(vidId, lang)
    text = text.decode("utf-8")
    if text == '':
        return ('bad request, ' + str(lang) + " subtitles not found"), 400
    subsarray, totaltime = youtubeParser.get_captions(text)
    dict = dictionaries.getdictionarybysuffix(signlang)
    if dict is None:
        return 'bad request, language pair not found', 400
    language = signlang[0:2]
    filename = PoseCreator.create_pose_for_youtube(dict, subsarray, signlang, language, totaltime, vidId)
    try:
        with open(filename, 'rb') as bites:
            return send_file(
                io.BytesIO(bites.read()),
                attachment_filename='po.pose',
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


dictionaries = PoseCreator.create_languages_to_suffix_dictionary()
dictionaries.createAllWordToID()
for dic in dictionaries.dictionaries:
    dic.dict_array = Dictionary.create_length_Array(dic.wordToID)
print("loaded index file and all dictionaries")
app.run(host="0.0.0.0", port=4002, threaded=True)
#app.run(port=4001, threaded=True)
# data = request.json
# lang = data["language"]
# subtitlesad = (data["url"])
# signlang = (data["signlang"])
