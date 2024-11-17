package com.example.aiview.chat.service;

public class MockOpenAIService extends OpenAIService{

    @Override
    public String transcribeAudioToText(byte[] audioData) {
        return "This is a mocked transcription";
    }

    @Override
    public String fetchAIResponse(String prompt) {
        return "This is a mocked AI response";
    }

    @Override
    public byte[] synthesizeAudioFromText(String text) {
        return "mocked-audio-data".getBytes();
    }
}
