from flask import Flask, render_template, request, jsonify
from registration_assistant import RegistrationAssistant

app = Flask(__name__)

assistant = RegistrationAssistant()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "response": "Please enter a message."
        })

    response = assistant.handle_message(message)

    return jsonify({
        "response": response
    })


@app.route("/reset", methods=["POST"])
def reset():
    assistant.reset()

    return jsonify({
        "response": "Registration session has been reset."
    })


if __name__ == "__main__":
    app.run(debug=True)