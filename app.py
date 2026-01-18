from flask import Flask, jsonify, render_template, request, session
from webAdventureMain import (
    generate_intro_story_chunks,
    generate_next_story_chunks,
    generate_conclusion_chunks,
)
import secrets
from geminiPrompt import geminiPrompt

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route("/")
def index():
    return render_template("site.html")

@app.route("/start")
def start():
    try:
        chunks, full_story, needed_type = generate_intro_story_chunks()
        session["story"] = full_story
        session["turn"] = 1
        session["needed_type"] = needed_type  # Initialize needed_type in session
        return jsonify({"chunks": chunks, "is_over": False})
    except Exception as e:
        print("Error in /start:", e)
        return jsonify({"chunks": ["⚠️ Failed to start the game."], "is_over": True}), 500

@app.route("/pi_action", methods=["GET"])
def pi_action():
    needed_type = session.get("needed_type")
    if needed_type is None:
        return jsonify({"text": None}), 204  # nothing to wait for yet

    # Blocks until the correct physical button is pressed:
    text = geminiPrompt(int(needed_type))
    return jsonify({"text": text})

@app.route("/input", methods=["POST"])
def handle_input():
    try:
        data = request.get_json(silent=True) or {}
        user_input = (data.get("text") or "").strip()

        story_so_far = session.get("story", "")
        turn = session.get("turn", 1)

        if not story_so_far:
            return jsonify({"chunks": ["⚠️ Session lost. Please refresh to restart."], "is_over": True}), 400

        if turn >= 5:
            return jsonify({"chunks": ["⚠️ The story is already finished. Refresh to play again."], "is_over": True}), 400

        next_block_number = turn + 1

        if next_block_number == 5:
            chunks, new_text = generate_conclusion_chunks(story_so_far)
            session["story"] = (story_so_far + " " + new_text).strip()
            session["turn"] = 5
            session.pop("needed_type", None)  # Clear needed_type as story is over
            return jsonify({"chunks": chunks, "is_over": True})

        chunks, new_text, needed_type = generate_next_story_chunks(story_so_far, user_input, turn)
        session["story"] = (story_so_far + " " + new_text).strip()
        session["turn"] = next_block_number
        session["needed_type"] = needed_type

        return jsonify({"chunks": chunks, "is_over": False})

    except Exception as e:
        print("Error in /input:", e)
        return jsonify({"chunks": ["⚠️ Something went wrong processing your input."], "is_over": False}), 500

if __name__ == "__main__":
    app.run(debug=True)
