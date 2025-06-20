from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)           # create the web-app object


@app.route("/")                 # run this function at http://127.0.0.1:5000/
def home():
    # pass the current year to the footer placeholder in layout.html
    return render_template("index.html", year=datetime.now().year)


if __name__ == "__main__":
    # debug=True => auto-reload on every file-save
    app.run(debug=True)