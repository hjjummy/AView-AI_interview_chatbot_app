from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os

# Flask 앱 설정
app = Flask(__name__)
app.secret_key = "your_secret_key"  # 세션 암호화 키
CORS(app)  # CORS 설정

# 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite DB 경로
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 데이터베이스 모델 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# 데이터베이스 초기화
with app.app_context():
    db.create_all()

# 회원가입 엔드포인트
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    # 이메일 중복 확인
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    # 비밀번호 해싱 후 저장
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# 로그인 엔드포인트
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # 사용자 검색
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # 로그인 성공 시 세션 저장
    session['user_id'] = user.id
    session['user_name'] = user.name

    return jsonify({"message": "Login successful", "user": {"id": user.id, "name": user.name}})

# 로그아웃 엔드포인트
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"})

# 현재 로그인 상태 확인
@app.route('/me', methods=['GET'])
def me():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.get(user_id)
    return jsonify({"user": {"id": user.id, "name": user.name, "email": user.email}})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
