from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import firebase_admin
from firebase_admin import credentials, auth
import promptagent
cred = credentials.Certificate("alixer-352b3-firebase-adminsdk-fbsvc-b9d0ad5897.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.secret_key = "supersecretkey"  

@app.route("/")
def home():
    if "user" in session:
        return render_template("home.html", user=session["user"])
    return render_template("index.html")


@app.route("/auth")
def auth_route():
    return render_template("auth.html")


@app.route("/sessionLogin", methods=["POST"])
def session_login():
    data = request.get_json()
    id_token = data.get("idToken")

    try:
        decoded_token = auth.verify_id_token(id_token)
        session["user"] = decoded_token
        return jsonify({"message": "Login successful!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    





@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/protected")
def protected():
    if "user" not in session:
        return redirect(url_for("home"))
    return f"Protected content for {session['user']['email']}."




@app.route("/generate_prompt", methods=["POST"])
def generate_prompt():
    data = request.get_json()
    user_input = data.get("prompt", "").strip()

    if not user_input:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    system_prompt = (
        "You are a professional English prompt refiner. "
        "Your task is to take the user's raw message and rewrite it into a clear, "
        "grammatically correct, and well-structured prompt for a design generation agent. "
        "Do not include formatting symbols such as asterisks, hashtags, or markdown. "
        "Do not make any design or layout suggestions yourself. "
        "Simply transform the user's message into a polished, unambiguous prompt "
        "that the design agent can easily interpret. "
        "At the end of the prompt, include this instruction exactly: "
        "'Generate 4 design variations based on this prompt.'"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    response, error = promptagent.call_ai_api(messages)

    if error:
        return jsonify({"error": error}), 500
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True) 

    