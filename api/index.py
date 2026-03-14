from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder="../templates")

@app.route("/", methods=["GET", "POST"])
def home():
    ai_result = None

    if request.method == "POST":
        file = request.files.get("resume")

        if file:
            
            filepath = os.path.join("uploads", file.filename)
            os.makedirs("uploads", exist_ok=True)
            file.save(filepath)

            # Temporary result
            ai_result = "Resume uploaded successfully! AI analysis will come here."

    return render_template("index.html", ai_result=ai_result)

if __name__ == "__main__":
    app.run()
