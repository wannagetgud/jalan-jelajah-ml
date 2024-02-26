from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from cbf import recommend_by_content_based_filtering

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@cross_origin()
@app.route("/", methods=["GET"])
def halo():
    return "Halo"


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    recommendations = recommend_by_content_based_filtering(data["category"], data["city"], data["count"])
    for place in recommendations:
        place["price"] = int(place["price"])
    return jsonify(recommendations)
    # return recommendations


if __name__ == "__main__":
    app.run(debug=True)
