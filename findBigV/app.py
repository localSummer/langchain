from flask import Flask, render_template, request, jsonify
from findbigV import find_bigV
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process", methods=["POST"])
def process():
    flower = request.form["flower"]
    response_str = find_bigV(flower)
    response = json.loads(response_str)
    
    return jsonify({
        "summary": response["summary"],
        "facts": response["facts"],
        "interest": response["interest"],
        "letter": response["letter"],
    })
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)