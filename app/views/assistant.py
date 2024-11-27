import io
from datetime import datetime
from flask import Blueprint, Flask, request, jsonify, send_file, session, redirect

from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS
import time
from pathlib import Path

import os
import logging
import requests

# .env 파일에서 환경 변수 로드
load_dotenv()
bp = Blueprint('assistant', __name__, url_prefix='/')

# OpenAI API 키 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TTS_API_URL = "https://api.openai.com/v1/audio/generate"

app = Flask(__name__)
app.secret_key = "your_secret_key"  # 세션 암호화 키
# 세션 사용 없이 interview의 db에 assistant와 thread id를 저장하는 방법도

# CORS 설정 (필요시 origins를 특정 도메인으로 제한 가능)
CORS(app)
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/', methods=['GET'])
def index():
    return redirect('/send_resume')

# OpenAI API 호출을 위한 엔드포인트
@app.route('/send_resume', methods=['POST'])
# @token_required
def send_message_init():
    if request.method == 'POST':
        print("POST request received")

    data = request.form
    if not data:
        return jsonify({"error": "request is required"}), 400
    else:
        print("good")

    file = request.files.get('resume')

    if 'resume' not in request.files:
        return jsonify({"error": "No selected file"}), 400

    # 파일을 서버에 저장하거나 처리
    file_path = os.path.join(r"D:\aiview_flask\projects\myproject\uploads", file.filename)
    print(file_path)
    file.save(file_path)

    gender = data.get('gender')
    age = data.get('age')

    instruction = f"""업로드된 자기소개서의 내용을 기반으로 엄격한 압박 면접을 진행하는 면접관 역할을 맡아주세요. 실제 면접처럼 한가지의 질문 혹은 요청을 합니다.
    사용자의 성별은 {gender}이며, 나이는 {age}입니다.
첫시작은 안녕하세요 000지원자씨 면접 시작하겠습니다. 먼저 간단하게 자기소개 부탁드립니다. 라고 시작해.
내가 답변을 하면 나의 답변이 업로드한 자기소개서 pdf 파일 내용과 일치하는지 확인하고, 면접 과정에서 모호하거나 구체적인 설명이 부족한 부분이 있다면 추가 질문을 해주세요. 이때도 한가지만 질문합니다. 또한, 자기소개서에 드러나지 않은 내 전공 분야나 관련된 지식에 대해서도 깊은 이해를 평가할 수 있는 질문을 해주세요.
# Steps

1. **자기소개서 분석**: 내가 업로드한 자기소개서 내용을 바탕으로 주요 이슈나 질문 거리가 될 만한 부분을 도출하세요.
2. **답변 검증 및 질문**: 내가 면접 과정에서 한 답변이 자기소개서의 내용과 일치하는지 확인하고, 모호한 부분이 있다면 다시 질문하거나 이유를 물어봐 주세요.
3. **깊이 있는 추가 질문**: 내 분야와 관련된 지식에 대한 질문을 통해 나의 이해도를 검증하는 질문을 해주세요.
4. **압박 면접 진행**: 편안함을 허용하지 않는 방향으로, 내가 준비되지 않았을 것으로 보일만한 질문이나 예상치 못한 질문을 통해 차분하지만 압박적인 면접을 진행하세요.

# Output Format

다음과 같은 형식으로 진행해주세요:
- 질문 형태로 나에게 한가지 질문을 먼저 해주세요.
- 내가 대답을 하면, 그 대답이 자기소개서와 일치하는지 여부와 함께 추가로 궁금한 점을 지적하거나 다른 질문을 이어가주세요.
- 질문과 검토가 모두 이루어진 후, 결론적으로 나의 답변 평가 또는 조언도 짧게 제공해주세요.  반드시 면접 대화 느낌이 나게 한번에 하나씩 질문해야함 Examples 형식에 맞게 질문해


# Notes

- 가능한 한 압박적인 질문을 지속하며 진정성 있는 답변을 유도해주세요.
- 답변의 모호함이나 어느 정도 준비되지 않은 부분에 대해 의도적으로 도전적인 질문을 해주세요.
- 나의 분야에 대해 심도 있는 질문을 던질 때에는 자기소개서의 내용을 기반으로 파생된 점에 초점을 맞춰주세요.
- 한국어로 질문하세요.
- 서로 상호작용을 하며 면접이 이루어져야합니다. 한번 말할 때 한가지의 질문을 합니다."""




    # Assistant OpenAI API 호출
    # step 1. assistant 생성
    assistant = client.beta.assistants.create(
        name="aiview",
        instructions=instruction,
        tools=[{"type": "file_search"}],
        model="gpt-4o",
    )
    # step 2. thread 생성
    thread = client.beta.threads.create()

    # 생성된 assistant와 thread를 세션에 저장
    session['assistant'] = assistant.id
    session['thread'] = thread.id

    # 자소서 파일 저장
    vector_store = client.beta.vector_stores.create(name="storage")

    file_paths = [file_path]
    file_streams = [open(path, "rb") for path in file_paths]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    try:
        assistant = client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="안녕하세요. 질문 시작해 주세요."
            # 추가 instruction 첨부 가능
        )
        print(message)

        # run 실행
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
        # RUN이 completed 되었나 1초마다 체크
        while run.status != "completed":
            print("status 확인 중", run.status)
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        # while문을 빠져나왔다는 것은 완료됐다는 것이니 메세지 불러오기
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )

        response_data = messages.data[0]
        print("OpenAI Response json: ", response_data)
        response = response_data.content[0].text.value
        # print("OpenAI Response:", response)
        # OpenAI의 응답을 클라이언트로 전달
        # { response : "생성한 응답 텍스트" }

        botResponse = TTSAPI(response)
        # botResponse : audio(응답텍스트)
        # return jsonify("botResponse : ", str(botResponse))
        return send_file(
            botResponse,
            mimetype='audio/mpeg',  # 음성 파일 형식 지정(MP3)
            as_attachment=False  # 다운로드가 아닌 단순 전송
        )

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Error communicating with OpenAI API"}), 500

    # finally:
    #     # 파일 전송 후 삭제 (성공적으로 전송한 경우에도 삭제)
    #     if os.path.exists(botResponse):
    #         os.remove(botResponse)
    #         print(f"File {botResponse} has been deleted.")

@app.route('/send_message', methods=['POST'])
# @token_required
def send_message():
    data = request.form

    if not data:
        return jsonify({"error": "message is required"}), 400

    message = data.get('message')

    # 먼저 session에서 assistant와 thread를 가져오기
    assistant = session.get('assistant')
    thread = session.get('thread')

    if not assistant or not thread:
        return jsonify({"error": "Assistant and thread must be initialized first using /send_resume"}), 400

    try:
        # step 3. thread에 message 전송
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content= message
        )

        # run 실행
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
        # RUN이 completed 되었나 1초마다 체크
        while run.status != "completed":
            print("status 확인 중", run.status)
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        # while문을 빠져나왔다는 것은 완료됐다는 것이니 메세지 불러오기
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        response_data = messages.data[0]
        print("OpenAI Response json: ", response_data)
        response = response_data.content[0].text.value

        # OpenAI의 응답을 클라이언트로 전달
        # { response : "생성한 응답 텍스트" }
        botResponse = TTSAPI(response)
        return send_file(
            botResponse,
            mimetype='audio/mpeg',  # 음성 파일 형식 지정(MP3)
            as_attachment=False  # 다운로드가 아닌 단순 전송
        )

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": "Error communicating with OpenAI API"}), 500

def TTSAPI(message):
    try:
        # 타임스탬프를 이용하여 고유한 파일 이름 생성
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        speech_file_path = Path(__file__).parent / f"speech_{timestamp}.mp3"
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=message,
        )
        # 스트리밍 방식으로 응답을 파일로 저장
        with open(speech_file_path, 'wb') as f:
            response.with_streaming_response(f.write)
        return speech_file_path

    except requests.exceptions.RequestException as e:
        print( f"Error: {e}")
        raise Exception("Error communicating with TTS API")

if __name__ == '__main__':
    # 서버 실행
    app.run(debug=True,host = '0.0.0.0', port=3000)
