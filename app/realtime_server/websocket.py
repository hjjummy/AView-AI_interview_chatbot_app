import os
import json
from projects.myproject.app.realtime_server.websocket import WebSocketApp

# WebSocket URL
url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"

# WebSocket 열릴 때 호출되는 함수
def on_open(ws):
    print("서버에 연결되었습니다.")
    message = {
        "type": "response.create",
        "response": {
            "modalities": ["text"],
            "instructions": "사용자를 도와주세요."
        }
    }
    ws.send(json.dumps(message))

# WebSocket 메시지를 받을 때 호출되는 함수
def on_message(ws, message):
    print(json.loads(message))

# WebSocket 설정
headers = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "OpenAI-Beta": "realtime=v1",
}

ws = WebSocketApp(url, on_open=on_open, on_message=on_message, header=headers)

# WebSocket 연결 시작
ws.run_forever()
