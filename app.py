from flask import Flask, request, jsonify, send_from_directory
import os
import base64
from tts_engine import generate_google_tts

# Google TTS için key dosyasını yükle.
if "GOOGLE_CREDENTIALS_B64" in os.environ:
    key_data = base64.b64decode(os.environ["GOOGLE_CREDENTIALS_B64"])
    with open("google-tts-key.json", "wb") as f:
        f.write(key_data)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-tts-key.json"

app = Flask(__name__)
STATIC_DIR = os.path.join(os.getcwd(), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

@app.route("/")
def index():
    return "Lingroot TTS API is running."

@app.route("/tts", methods=["POST"])
def tts():
    try:
        data = request.get_json()
        text = data.get("text")
        voice = data.get("voice", "en-US-Wavenet-D")

        if not text:
            return jsonify({"error": "Text verisi zorunludur."}), 400

        output_path = os.path.join(STATIC_DIR, "output.mp3")
        generate_google_tts(text, voice_name=voice, output_path=output_path)

        return jsonify({
            "status": "ok",
            "audio_url": request.host_url + "static/output.mp3"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
