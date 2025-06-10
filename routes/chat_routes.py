from flask import Blueprint, request, session, jsonify, render_template, current_app
from openai import OpenAI
from config import *
from manual_utils import get_relevant_chunks

chat_bp = Blueprint("chat", __name__)
client = OpenAI(api_key=OPENAI_API_KEY)


@chat_bp.route("/")
def chat_home():
    if "history" not in session:
        session["history"] = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
        session["history"].append({"role": "assistant", "content": STARTING_MESSAGE})

    filtered_history = [msg for msg in session.get("history", []) if msg["role"] != "system"]
    return render_template("chat.html", history=filtered_history)



@chat_bp.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    user_input = data.get("user_input", "")
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"reply": "User ID missing"}), 400

    index = current_app.index
    chunks = current_app.chunks

    if not index or not chunks:
        return jsonify({"reply": "PDF knowledge base is not available"}), 500

    relevant_chunks = get_relevant_chunks(user_input, index, chunks)
    context = "\n\n".join(relevant_chunks)

    # No extra tone override here, just informative context
    user_prompt = f"""
Here be some nuggets of wisdom from the ship's log:

{context}

Now answer this, ye scurvy dog: {user_input}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": user_prompt}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500
