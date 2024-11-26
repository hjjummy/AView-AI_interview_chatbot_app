from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print("OpenAI API Key:", OPENAI_API_KEY)  # API 키 출력 (로그로 확인)

app = Flask(__name__)

# CORS 설정 (필요시 origins를 특정 도메인으로 제한 가능)
CORS(app)

# OpenAI API 호출을 위한 엔드포인트
@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # OpenAI API 호출
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": message}]
            }
        )
        response.raise_for_status()  # 에러 발생 시 예외 던지기
        response_data = response.json()
        # OpenAI의 응답을 클라이언트로 전달
        return jsonify({"response": response_data['choices'][0]['message']['content']})
    except requests.exceptions.RequestException as e:
        print(e)
        return jsonify({"error": "Error communicating with OpenAI API"}), 500

if __name__ == '__main__':
    # 서버 실행
    app.run(debug=True, port=3000)
