# from flask import Flask, request, Response, jsonify
# import soundfile as sf
# import io
# from kokoro import KPipeline, KModel

# app = Flask(__name__)
# mymodel = KModel(model="C:/Users/HP/Downloads/kokoro-v1_0.pth")

# # Create pipeline with the local model
# pipeline = KPipeline(
#     lang_code='a',
#     model=mymodel,
#      # important: disable HuggingFace repo fetching
# )

# @app.route("/")
# def home():
#     return jsonify({"message": "Kokoro TTS API is running 🚀"})

# @app.route("/tts", methods=["POST"])
# def tts():
#     data = request.get_json()
#     text = data.get("text", "")
#     voice = data.get("voice", "af_heart")

#     if not text:
#         return jsonify({"error": "No text provided"}), 400

#     def generate_wav():
#         # Write WAV header first
#         buf = io.BytesIO()
#         with sf.SoundFile(buf, mode="w", samplerate=24000, channels=1, format="WAV") as f:
#             for _, _, audio in pipeline(text, voice=voice):
#                 f.write(audio)        # write chunk by chunk
#                 yield buf.getvalue()  # stream what we have so far
#                 buf.seek(0)
#                 buf.truncate(0)

#     return Response(generate_wav(), mimetype="audio/wav")

# @app.route("/voice")
# def voice():
#     voices = {
#         "female": ["af_heart", "af_alloy", "af_aoede", "af_bella", "af_jessica"],
#         "male": ["am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam"]
#     }
#     return jsonify({"voice": voices})


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)



# import os
# import io
# from flask import Flask, request, Response, jsonify
# import soundfile as sf
# import gdown
# from kokoro import KPipeline, KModel

# app = Flask(__name__)

# # -------------------------------
# # 1️⃣ Create a directory for the model
# # -------------------------------
# MODEL_DIR = "models"
# os.makedirs(MODEL_DIR, exist_ok=True)

# MODEL_URL = "https://drive.google.com/uc?id=1cH5RMyRFrJMWqsr0i5n75SujZTyRSi2N"
# MODEL_PATH = os.path.join(MODEL_DIR, "kokoro-v1_0.pth")

# if not os.path.exists(MODEL_PATH):
#     print("Downloading Kokoro model...")
#     gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

# # -------------------------------
# # 2️⃣ Load full model
# # -------------------------------
# mymodel = KModel(model=MODEL_PATH, disable_complex=True)
# pipeline = KPipeline(lang_code='a', model=mymodel)

# # -------------------------------
# # 3️⃣ Routes
# # -------------------------------
# @app.route("/")
# def home():
#     return jsonify({"message": "Kokoro TTS API is running 🚀"})

# @app.route("/tts", methods=["POST"])
# def tts():
#     data = request.get_json()
#     text = data.get("text", "")
#     voice = data.get("voice", "af_heart")

#     if not text:
#         return jsonify({"error": "No text provided"}), 400

#     def generate_wav():
#         buf = io.BytesIO()
#         with sf.SoundFile(buf, mode="w", samplerate=24000, channels=1, format="WAV") as f:
#             for _, _, audio in pipeline(text, voice=voice):
#                 f.write(audio)
#                 yield buf.getvalue()
#                 buf.seek(0)
#                 buf.truncate(0)

#     return Response(generate_wav(), mimetype="audio/wav")

# @app.route("/voice")
# def voice():
#     voices = {
#         "female": ["af_heart", "af_alloy", "af_aoede", "af_bella", "af_jessica"],
#         "male": ["am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam"]
#     }
#     return jsonify({"voice": voices})

# # -------------------------------
# # 4️⃣ Run app
# # -------------------------------
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

import os
import io
from flask import Flask, request, Response, jsonify
import soundfile as sf
import gdown
from kokoro import KPipeline, KModel

app = Flask(__name__)

# -------------------------------
# 1️⃣ Model setup
# -------------------------------
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Google Drive "shareable link" converted to direct download
MODEL_URL = "https://drive.google.com/uc?id=1cH5RMyRFrJMWqsr0i5n75SujZTyRSi2N"
MODEL_PATH = os.path.join(MODEL_DIR, "kokoro-v1_0.pth")

# Download only if not present
if not os.path.exists(MODEL_PATH):
    print("Downloading Kokoro model from Google Drive...")
    gdown.download(MODEL_URL, MODEL_PATH, quiet=False)

# -------------------------------
# 2️⃣ Load model
# -------------------------------
mymodel = KModel(model=MODEL_PATH, disable_complex=True)
pipeline = KPipeline(lang_code='a', model=mymodel)

# -------------------------------
# 3️⃣ Routes
# -------------------------------
@app.route("/")
def home():
    return jsonify({"message": "Kokoro TTS API is running 🚀"})

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "")
    voice = data.get("voice", "af_heart")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    def generate_wav():
        buf = io.BytesIO()
        with sf.SoundFile(buf, mode="w", samplerate=24000, channels=1, format="WAV") as f:
            for _, _, audio in pipeline(text, voice=voice):
                f.write(audio)
                yield buf.getvalue()
                buf.seek(0)
                buf.truncate(0)

    return Response(generate_wav(), mimetype="audio/wav")

@app.route("/voice")
def voice():
    voices = {
        "female": ["af_heart", "af_alloy", "af_aoede", "af_bella", "af_jessica"],
        "male": ["am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam"]
    }
    return jsonify({"voice": voices})

# -------------------------------
# 4️⃣ Run app
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
