import os
import base64
import numpy as np
import soundfile as sf
from flask import Flask, jsonify

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

@app.route('/process-audio-files', methods=['POST'])
def process_audio_files():
    try:
        # List of file paths (mocked for this example)
        files = [
            './path/to/sample1.wav',
            './path/to/sample2.wav',
            './path/to/sample3.wav'
        ]

        base64_audio_chunks = []

        # Read and process each audio file
        for filename in files:
            audio_data, samplerate = sf.read(filename, dtype='float32')

            # Ensure mono audio
            if len(audio_data.shape) > 1:
                audio_data = audio_data[:, 0]  # Use only the first channel

            # Convert to Base64 PCM16
            base64_chunk = base64_encode_audio(audio_data)
            base64_audio_chunks.append({
                "type": "input_audio_buffer.append",
                "audio": base64_chunk
            })

        # Create the response to simulate WebSocket messages
        response = {
            "messages": base64_audio_chunks + [
                {"type": "input_audio_buffer.commit"},
                {"type": "response.create"}
            ]
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
