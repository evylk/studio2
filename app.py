from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_dalle_prompt(phrase):
    words = phrase.split("-")
    return (
        f"Create a colorful, friendly 3D animated movie scene for teens (ages 13-18) where a single character interacts with elements "
        f"inspired by the words: '{words[0]}', '{words[1]}', and '{words[2]}'. "
        f"Avoid surreal or dreamlike abstraction. Keep it fun, clear as if part of a Pixar or Disney movie setting."
        f"Choose one of the 3 words as a character keep it simple."
        f"Absolutely no generation of anything that resembles ASCII characters or symbols."    
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/image", methods=["POST"])
def image():
    data = request.get_json()
    phrase = data.get("passphrase")
    if not phrase:
        return jsonify({"error": "Missing passphrase"}), 400

    prompt = generate_dalle_prompt(phrase)

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        image_url = response.data[0].url
        return jsonify({"url": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
