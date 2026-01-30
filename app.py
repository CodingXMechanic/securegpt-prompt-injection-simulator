# -*- coding: utf-8 -*-
# app.py
from flask import Flask, render_template, request, jsonify
from simulator import LLMSimulator
from attacks import ATTACKS, ATTACK_DESCRIPTIONS

app = Flask(__name__, static_folder="static", template_folder="templates")

def load_system_prompt():
    with open("system_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

llm = LLMSimulator(load_system_prompt())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    body = request.json or {}
    user_input = body.get("prompt", "")
    response = llm.generate_response(user_input)
    return jsonify({"response": response})

@app.route("/attacks", methods=["GET"])
def attacks():
    return jsonify({"attacks": ATTACKS, "descriptions": ATTACK_DESCRIPTIONS})

@app.route("/mode", methods=["GET"])
def get_mode():
    return jsonify({"mode": llm.mode})

@app.route("/set_mode", methods=["POST"])
def set_mode():
    body = request.json or {}
    mode = body.get("mode")
    if mode not in ("vulnerable", "hardened"):
        return jsonify({"error": "invalid mode"}), 400

    archived = llm.archive_current_conversation(new_mode=mode)
    return jsonify({"status": "ok", "mode": llm.mode, "archived": archived})

@app.route("/conversations", methods=["GET"])
def conversations():
    return jsonify({"conversations": llm.get_conversation_summaries()})

@app.route("/conversation", methods=["GET"])
def conversation():
    convo_id = request.args.get("id")
    if not convo_id:
        return jsonify({"error": "id required"}), 400
    convo = llm.get_conversation_by_id(convo_id)
    if not convo:
        return jsonify({"error": "not found"}), 404
    return jsonify({"conversation": convo})

@app.route("/history", methods=["GET"])
def history():
    return jsonify({"history": llm.history})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)