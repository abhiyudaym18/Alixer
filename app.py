from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import firebase_admin
from firebase_admin import credentials, auth
import designagent
import config

cred = credentials.Certificate(config.credential)
firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.secret_key = config.security_key 

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




@app.route("/generate_design", methods=["POST"])
def generate_design():
    data = request.get_json()
    user_input = data.get("prompt", "").strip()

    if not user_input:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    result, error = designagent.process_design_request(user_input)

    if error:
        return jsonify({"error": error}), 500
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True) 

    