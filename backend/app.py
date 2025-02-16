from flask import Flask, request
from db import db
from routes import routes
from datetime import datetime
from models import AccessAttempt

app = Flask(__name__)

# Подключаем базу данных
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@db:5432/honeypot"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.register_blueprint(routes)

# LOG  REQUEST
@app.before_request
def log_access_attempt():
    ip = request.remote_addr  
    port = request.environ.get('REMOTE_PORT') 
    timestamp = datetime.now()

    # LOG ATTEMPT
    attempt = AccessAttempt(
        timestamp=timestamp,
        ip=ip,
        port=port,
        data="Scan attempt logged"
    )
    db.session.add(attempt)
    db.session.commit()

@app.route('/')
def home():
    return "Welcome to Honeypot!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)

