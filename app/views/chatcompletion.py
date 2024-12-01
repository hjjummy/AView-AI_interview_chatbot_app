import json
from flask import Blueprint, jsonify, logging , Flask
from openai import OpenAI
from dotenv import load_dotenv
import os

# Flask Blueprint 설정
recommend_bp = Blueprint('recommendation', __name__, url_prefix='/recommend')

#환경변수 로드
load_dotenv()

# OpenAI API 키
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

if OPENAI_API_KEY:
    print("OPENAI_API_KEY successfully loaded.")
else:
    print("Failed to load OPENAI_API_KEY. Check your .env file.")

# 데이터 저장 경로
DATA_STORE_PATH = "data_store.json"

def load_data_from_file():
    """로컬 파일에서 데이터 로드"""
    if os.path.exists(DATA_STORE_PATH):
        with open(DATA_STORE_PATH, "r") as f:
            return json.load(f)
    return {}

@recommend_bp.route('/analyze', methods=['POST'])
def analyze_responses():
    """사용자 답변 분석 및 개선"""
    print("Received request at /recommend/analyze")  # 디버깅용 로그
    session_data = load_data_from_file()

    if not session_data.get('assistant_id') or not session_data.get('thread_id'):
        print("No session data found")  # 디버깅용 로그
        return jsonify({"error": "No session data found"}), 400

    assistant_id = session_data['assistant_id']
    thread_id = session_data['thread_id']

    try:
        # 쓰레드 메시지 가져오기
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        user_responses = [msg for msg in messages.data if msg.role == "user"]

        if not user_responses:
            return jsonify({"error": "No user responses found"}), 400

        # 사용자 답변 추출
        user_answers = "\n\n".join([msg.content for msg in user_responses])

        # ChatCompletion 호출
        instruction = """
        아래는 사용자의 면접 답변입니다. 답변을 분석하고 개선점을 제공하세요.
        - 원래 답변: <사용자 답변>
        - 보완할 점: <간단한 피드백>
        - 추천 답변: <추천 형식>
        """
        prompt = instruction + user_answers

        chat_response = client.completions.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=1000,
            temperature=0.7,
        )

        # 응답 처리
        recommended_answers = chat_response.choices[0].text.strip()
        return jsonify({"recommendations": recommended_answers}), 200

    except Exception as e:
        logging.error(f"Error during analysis: {str(e)}")
        return jsonify({"error": "Error analyzing responses"}), 500
# Flask 애플리케이션 설정 및 실행
app = Flask(__name__)

# Blueprint 등록
app.register_blueprint(recommend_bp)

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True, host="0.0.0.0", port=3000)
