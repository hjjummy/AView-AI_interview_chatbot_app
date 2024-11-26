import base64
import numpy as np
import soundfile as sf
from flask import Flask, request, jsonify

app = Flask(__name__)


# Converts Float32 numpy array to PCM16 bytes
def float_to_16bit_pcm(float32_array):
    pcm16_array = np.int16(np.clip(float32_array, -1, 1) * 32767)
    return pcm16_array.tobytes()


# Converts Float32 numpy array to Base64-encoded PCM16 data
def base64_encode_audio(float32_array):
    pcm16_bytes = float_to_16bit_pcm(float32_array)
    base64_audio = base64.b64encode(pcm16_bytes).decode('utf-8')
    return base64_audio


@app.route('/process-audio', methods=['POST'])
def process_audio():
    try:
        # Load audio file from request
        file = request.files['audio']
        audio_data, samplerate = sf.read(file, dtype='float32')

        # Ensure mono audio
        if len(audio_data.shape) > 1:
            audio_data = audio_data[:, 0]  # Use only the first channel

        # Convert to Base64 PCM16
        base64_audio_data = base64_encode_audio(audio_data)

        # Prepare the event
        event = {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "audio": base64_audio_data
                    }
                ]
            }
        }

        # Send the response back
        return jsonify(event)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
