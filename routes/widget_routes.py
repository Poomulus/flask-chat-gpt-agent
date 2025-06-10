from flask import Blueprint, render_template, request, jsonify
from config import *
import os

widget_bp = Blueprint("widget", __name__)
user_histories = {} 

@widget_bp.route("/widget-chat/<user_id>")
def widget_chat(user_id):
    history = user_histories.get(user_id)
    if not history:
        user_histories[user_id] = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
        history = []
    display_history = [{"role": "assistant", "content": STARTING_MESSAGE}] + [
        msg for msg in history if msg["role"] != "system"
    ]
    return render_template("widget_chat.html", history=display_history)



@widget_bp.route("/widget.js")
def widget_js():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(base_dir, "..", "static", "widget_templates", "widget.js.template")

        with open(template_path, "r") as file:
            js_template = file.read()

        final_js = js_template.replace("{{DOMAIN}}", request.url_root.rstrip("/"))
        return final_js, 200, {"Content-Type": "application/javascript"}
    except Exception as e:
        return f"Error loading widget.js: {e}", 500





@widget_bp.route("/reset", methods=["POST"])
def widget_reset():
    data = request.get_json()
    user_id = data.get("user_id")

    if user_id and user_id in user_histories:
        del user_histories[user_id]

    return jsonify({"status": "reset"}), 200

