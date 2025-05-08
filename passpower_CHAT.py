from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import traceback

# Load environment variables from .env file
load_dotenv()

# Initialize Flask and OpenAI client
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Route: homepage
@app.route("/")
def index():
    return render_template("index.html")

# Helper function: get a valid passphrase
def generate_valid_passphrase():
    prompt = (
    "clear memory, start fresh."
    "Create a 3-word passphrase, each word separated with a hyphen"
    "Use words from eff.org current wordlist"
    "From these words ensure they are vocabulary appropriate for 13 year olds"
    "The total character count (excluding hyphens) must be at least 15. "
    "Return only the passphrase in this format: word1-word2-word3. No quotes, no extra text."
    "all lower case letters"
)


    for _ in range(3):  # Retry up to 3 times
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0,
            max_tokens=20
        )

        phrase = response.choices[0].message.content.strip()

        # Basic checks
        if phrase.count("-") == 2 and len(phrase.replace("-", "")) >= 15:
            return phrase

    # If none pass the check after retries
    raise ValueError("Passphrase is invalid or too short after multiple attempts.")

# Route: generate passphrase via GPT
@app.route("/generate-passphrase", methods=["POST"])
def generate_passphrase():
    try:
        phrase = generate_valid_passphrase()
        return jsonify({"passphrase": phrase})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    



@app.route("/scene", methods=["POST"])
def scene():
    try:
        data = request.get_json()
        phrase = data.get("passphrase")
        if not phrase:
            return jsonify({"error": "Missing passphrase"}), 400

        words = phrase.split("-")
        if len(words) != 3:
            return jsonify({"error": "Invalid passphrase format"}), 400

        prompt = (
            f"Write one simple sentence describing a scene for ages 13 to 18, "
            f"based on the words: '{words[0]}', '{words[1]}', and '{words[2]}'. "
            f"Use simple vocabulary, Only return the sentence."
        )

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=60
        )

        scene_description = response.choices[0].message.content.strip()
        return jsonify({"scene": scene_description})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/image", methods=["POST"])
def image():
    try:
        data = request.get_json()
        scene_description = data.get("scene")
        print("DALL·E prompt:", scene_description)

        if not scene_description:
            return jsonify({"error": "Missing scene description"}), 400

        # Add cartoon-style prompt tailoring (not shown to user)
        style_instruction = (
            "Style: colorful 3D animation, cartoon-like, Pixar or Disney-inspired. "
            "Avoid photo-realism. Use smooth lighting, expressive characters, and child-friendly design."
            "Add extra elements to enrich the scene."
        )

        # Final prompt sent to DALL·E
        final_prompt = f"{scene_description} -- {style_instruction}"

        dalle_response = client.images.generate(
            model="dall-e-3",
            prompt=final_prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )

        image_url = dalle_response.data[0].url
        return jsonify({"url": image_url, "scene": scene_description})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500












# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
