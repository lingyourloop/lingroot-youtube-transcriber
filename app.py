from flask import Flask, request, jsonify
from utils import process_youtube_link
import os
import base64

# Google TTS için JSON key dosyasını ortam değişkeninden oluştur
if "GOOGLE_CREDENTIALS_B64" in os.environ:
    key_data = base64.b64decode(os.environ["GOOGLE_CREDENTIALS_B64"])
    with open("google-tts-key.json", "wb") as f:
        f.write(key_data)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-tts-key.json"

app = Flask(__name__)

@app.route("/")
def index():
    return "Lingroot Transcribe API is running."

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        data = request.get_json()
        youtube_url = data.get("url")
        voice = data.get("voice", "en-US-Wavenet-D")

        if not youtube_url:
            return jsonify({"error": "YouTube linki gereklidir."}), 400

        result = process_youtube_link(youtube_url, voice)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
