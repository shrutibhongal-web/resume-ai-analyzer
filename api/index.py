from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder="../templates")

@app.route("/", methods=["GET", "POST"])
def home():
    ai_result = None

    if request.method == "POST":
        file = request.files.get("resume")

        if file:
            os.makedirs("uploads", exist_ok=True)
            filepath = os.path.join("uploads", file.filename)
            file.save(filepath)

            ai_result = "Resume uploaded successfully! 🎉"

    return render_template("index.html", ai_result=ai_result)
