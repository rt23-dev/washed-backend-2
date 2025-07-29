from flask import Flask
from routes.upload import upload_bp
from dotenv import load_dotenv
from routes.feedback import feedback_bp
from routes.upload import upload_bp
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)
app.register_blueprint(upload_bp)
app.register_blueprint(feedback_bp)

@app.route('/')
def home():
    return "Welcome to the WASHED backend!"

if __name__ == "__main__":
    app.run(debug=True)
