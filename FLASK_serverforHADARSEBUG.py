

from flask import (Flask,request,jsonify,send_file,make_response,abort)
import io


app = Flask(__name__)
number =0
@app.route("/pose",methods = ["GET"])
def get_pose():
    # file = request
    # with open('data.xml', 'w') as f:
    #     f.write(file.text)
    data  = request.get_data()
    with open('data.xml', 'wb') as f:
        f.write(data)
    #subsarray, suffix, language = TTMLParser.getArrfromCaptions("data.xml")
    #suffix = "en.us"
    # dict = dictionaries.getdictionarybysuffix(suffix)
    # main.create_pose_for_video(dict,subsarray, suffix, language)
    try:
        with open("po.pose", 'rb') as bites:
            return send_file(
                io.BytesIO(bites.read()),
                attachment_filename='hey.pose',
                mimetype='binary'
            )
    except FileNotFoundError:
        abort(404)


@app.route('/foo', methods=['GET'])
def foo():
    data = request.json
    lang  = data["language"]
    time = (data["subtitles"][0]["time"])
    return jsonify(data)

# langs = main.create_languages_to_suffix_dictionary()
# dictionaries = Dictionaries()
# for l in langs:
#     dict = Dictionary.PoseDictionary(l, langs[l])
#     dictionaries.add_dictionary(dict)
# dictionaries.createAllWordToID()
# print("loaded index file and all dictionaries")




app.run(port = 5000, threaded = True)