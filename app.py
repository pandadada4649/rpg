from flask import Flask, send_from_directory
from api.routes import bp

app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = "kaze_no_tabibito_2024"
app.register_blueprint(bp)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(debug=True)