import json
from flask import Flask
from flask_cors import CORS
from dotenv import dotenv_values
from utils.preprocess import extract_comments, evaluate_video
from utils.comments import get_comments

PORT = dotenv_values(".env")["FLASK_RUN_PORT"]

app = Flask(__name__)
CORS(app)  # enable CORS for all routes
        
@app.route("/model/<id>", methods=["GET"])
def index(id):
    comment = get_comments(id)
    if(len(comment) == 0):
        return {
            "data": "0"
        }
        
    comments = extract_comments(comment)
    score = evaluate_video(comments)
    
    score = json.dumps(str(score[0]))

    return {
        "data": score,
        "comments": comments[:10]
    }


if __name__ == '__main__':
    app.run(host="localhost", port=PORT, debug=True)
