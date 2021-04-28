import json
import main
from flask import (Flask,request,jsonify,send_file,make_response,abort)
import io
app = Flask(__name__)

@app.route("/pose",methods = ["GET"])
def return_pose():
    # file = request
    # with open('data.xml', 'w') as f:
    #     f.write(file.text)
    main.get_pose()
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

app.run(port=5000)