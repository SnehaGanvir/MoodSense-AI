from flask import Flask, jsonify, render_template, request

from emotion_model import detect_emotion


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/camera")
def camera():
    return render_template("camera.html")


@app.route("/result")
def result():
    mood = request.args.get("mood", "Neutral")
    confidence = request.args.get("confidence", "0")
    message = request.args.get("message", "Mood detection completed.")
    return render_template(
        "result.html",
        mood=mood,
        confidence=confidence,
        message=message,
    )


@app.route("/detect", methods=["POST"])
def detect():
    data = request.get_json(silent=True) or {}
    image_data = data.get("image")

    if not image_data:
        return jsonify({"error": "No image was received."}), 400

    try:
        result_data = detect_emotion(image_data)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Could not process the captured image."}), 500

    return jsonify(result_data)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
