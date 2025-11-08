from flask import Flask, request, jsonify, render_template, session, redirect, url_for, send_from_directory
import os
import firebase_admin
from firebase_admin import credentials, auth
import designagent
import codingagent
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
    # Check authentication
    if "user" not in session:
        return jsonify({"error": "Authentication required"}), 401

    # Get and validate prompt
    data = request.get_json()
    user_input = data.get("prompt", "").strip()
    if not user_input:
        return jsonify({"error": "Prompt cannot be empty"}), 400

    try:
        # Step 1: Get refined prompt and design plan
        result, error = designagent.process_design_request(user_input)
        if error:
            return jsonify({"error": f"Design planning failed: {error}"}), 500

        design_plan = result.get("design_plan")
        refined_prompt = result.get("refined_prompt")

        # Step 2: Generate HTML from design plan
        # Ensure the static/generated directory exists
        static_dir = os.path.join(app.root_path, "static")
        generated_dir = os.path.join(static_dir, "generated")
        os.makedirs(generated_dir, exist_ok=True)
        
        # Generate the HTML file
        output_path, error = codingagent.generate_html_from_design(
            design_plan, 
            output_dir=generated_dir
        )
        
        if error:
            return jsonify({"error": f"HTML generation failed: {error}"}), 500

        # Convert file path to URL path
        file_name = os.path.basename(output_path)
        generated_url = url_for('static', filename=f'generated/{file_name}')

        # Return success response with all data
        return jsonify({
            "refined_prompt": refined_prompt,
            "design_plan": design_plan,
            "generated_url": generated_url
        }), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/static/generated/<path:filename>')
def generated_file(filename):
    """Serve generated HTML files from static/generated directory"""
    return send_from_directory(
        os.path.join(app.root_path, 'static', 'generated'),
        filename
    )

if __name__ == "__main__":
    # Create static/generated directory at startup
    static_dir = os.path.join(app.root_path, "static")
    generated_dir = os.path.join(static_dir, "generated")
    os.makedirs(generated_dir, exist_ok=True)
    
    app.run(debug=True)