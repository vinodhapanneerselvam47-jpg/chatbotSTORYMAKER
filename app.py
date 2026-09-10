import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.1-flash-lite"

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in the .env file.")

client = genai.Client(api_key=API_KEY)

with open("chatbot_config", "r", encoding="utf-8") as config_file:
    SYSTEM_PROMPT = config_file.read().strip()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=f"{SYSTEM_PROMPT}\n\nUser: {message}",
        )

        reply = response.text.strip() if response.text else "I couldn't create a story right now."
        return jsonify({"reply": reply})

    except Exception as error:
        return jsonify({"error": f"Unable to generate a response: {error}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
