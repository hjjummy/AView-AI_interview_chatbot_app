import socketio
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import asyncio
import websockets
import os
import json
from flask import request
# from projects.myproject.app.as import socket_blueprint

API_URL = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# WebSocket 클라이언트를 관리하기 위한 딕셔너리
websocket_clients = {}

async def connect_to_openai(ws_id):
    try:
        # OpenAI WebSocket에 연결
        uri = API_URL
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
        websocket_clients[ws_id] = await websockets.connect(uri, extra_headers=headers)

        # 초기 요청 전송
        await websocket_clients[ws_id].send(json.dumps({
            "type": "response.create",
            "response": {
                "modalities": ["voice"],
                "instructions": "면접에서 예상 질문에 응답해 주세요.",
            }
        }))
    except Exception as e:
        print(f"Error connecting to OpenAI: {e}")
        if ws_id in websocket_clients:
            del websocket_clients[ws_id]

@socket_blueprint.route('/test', methods=['GET'])
def test_route():
    return {"message": "Blueprint is working!"}

@socketio.on('connect')
def handle_connect():
    print('New client connected')
    emit('connected', {'message': 'Connected to the server'})

@socketio.on('audio')
def handle_audio(data):
    ws_id = request.sid  # 클라이언트의 고유 ID
    if ws_id not in websocket_clients:
        asyncio.run(connect_to_openai(ws_id))

    async def send_audio():
        try:
            ws = websocket_clients[ws_id]
            # 음성 데이터를 OpenAI API로 전송
            await ws.send(json.dumps({
                "type": "input_audio_buffer.append",
                "audio": data
            }))
            await ws.send(json.dumps({"type": "input_audio_buffer.commit"}))

            # OpenAI로부터 응답 수신
            async for message in ws:
                parsed_message = json.loads(message)
                if (parsed_message["type"] == "response.generated" and
                        "output" in parsed_message["response"]):
                    emit('audio-response', parsed_message["response"]["output"]["audio"])
        except Exception as e:
            print(f"Error processing audio: {e}")

    asyncio.run(send_audio())


@socketio.on('disconnect')
def handle_disconnect():
    ws_id = request.sid
    print(f"Client disconnected: {ws_id}")
    if ws_id in websocket_clients:
        asyncio.run(websocket_clients[ws_id].close())
        del websocket_clients[ws_id]

