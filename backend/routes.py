from flask import Blueprint, request, jsonify
from db import db
from models import AccessAttempt
from datetime import datetime

routes = Blueprint('routes', __name__)

@routes.route('/attempts', methods=['GET'])
def get_attempts():
    attempts = AccessAttempt.query.all()
    return jsonify([
        {"timestamp": a.timestamp, "ip": a.ip, "port": a.port, "data": a.data} 
        for a in attempts
    ])

@routes.route('/attempt', methods=['POST'])
def log_attempt():
    data = request.json
    attempt = AccessAttempt(
        timestamp=datetime.now(),
        ip=data["ip"],
        port=data["port"],
        data=data.get("data", "")
    )
    db.session.add(attempt)
    db.session.commit()
    return jsonify({"message": "Logged"}), 201

