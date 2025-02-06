from flask import Flask
from flask_cors import CORS
from routes import routes

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'
CORS(app)
app.register_blueprint(routes)  # Register routes

if __name__ == '__main__':
    app.run(debug=True)
