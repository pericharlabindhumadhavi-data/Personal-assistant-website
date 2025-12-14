from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/assistant", methods=["POST"])
def assistant():
    user_input = request.json.get("message")

    if user_input.lower() == "hello":
        reply = "Hello! How can I help you?"
    elif user_input.lower() == "who are you":
        reply = "I am your personal assistant."
    else:
        reply = "Sorry, I did not understand that."

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
