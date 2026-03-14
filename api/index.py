from flask import Flask, render_template, request

app = Flask(__name__, template_folder="../templates")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        name = request.form.get("name")

        return render_template("result.html", name=name)

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
