package com.example.aiview.chat.controller;

import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.OpenAPI;
import com.example.aiview.chat.service.OpenAIService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/interview")
public class nnInterviewController {

    @Autowired
    private OpenAIService openAIService;

    @PostMapping(value = "/transcribe", consumes = MediaType.APPLICATION_OCTET_STREAM_VALUE)
    public ResponseEntity<String> transcribeAudioToText(@RequestBody byte[] audioData) {
        String text = openAIService.transcribeAudioToText(audioData);
        return ResponseEntity.ok(text);
    }

    @PostMapping("/fetchResponse")
    public ResponseEntity<String> fetchAIResponse(@RequestBody String prompt) {
        String aiResponse = openAIService.fetchAIResponse(prompt);
        return ResponseEntity.ok(aiResponse);
    }

    @PostMapping("/synthesizeAudio")
    public ResponseEntity<byte[]> synthesizeAudioFromText(@RequestBody String text) {
        byte[] audioData = openAIService.synthesizeAudioFromText(text);
        return ResponseEntity.ok().contentType(MediaType.APPLICATION_OCTET_STREAM).body(audioData);
    }
}
