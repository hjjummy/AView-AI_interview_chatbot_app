package com.example.aiview.chat.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.api.client.util.Value;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.springframework.stereotype.Service;

// 과정: 음성 -> 텍스트, 텍스트 -> 텍스트, 텍스트 -> 음성
@Service
public class OpenAIService {

    // OpenAI API 키 호출
    @Value("${openai.api.key}")
    private String apiKey;

    // objectMapper : JSON 형식의 응답을 자바 객체로 변환, 자바 객체를 JSON 형식으로 직렬화
    // => OpenAI의 응답을 처리할 때 유용
    private final ObjectMapper objectMapper = new ObjectMapper();

    // OpenAI Whisper API를 통해 음성(audioData)을 텍스트로 변환하는 메서드
    public String transcribeAudioToText(byte[] audioData) {
        String url = "https://api.openai.com/v1/audio/transcriptions";

        // OpenAI의 Whisper API 호출 및 응답 처리 로직
        // CloseableHttpClient: HTTP POST 요청 생성->OpenAI API로 데이터 전송->응답을 처리
        try (CloseableHttpClient client = HttpClients.createDefault()) {
            // HttpPost: URL, 헤더, 요청 본문을 설정->요청 전송->EntityUtils로 응답 데이터 가져옴
            HttpPost request = new HttpPost(url);
            request.setHeader("Authorization", "Bearer " + apiKey);
            request.setHeader("Content-Type", "application/json");

            StringEntity requestEntity = new StringEntity(
                    "{\"model\": \"whisper-1\", \"file\": " + objectMapper.writeValueAsString(audioData) + "}");
            request.setEntity(requestEntity);

            String responseString = EntityUtils.toString(client.execute(request).getEntity());
            JsonNode responseJson = objectMapper.readTree(responseString);
            // OpenAI Whisper API 가 반환현 JSON 응답에서 'text' 필드 추출해서 return
            return responseJson.get("text").asText();
        } catch (Exception e) {
            e.printStackTrace();
            return "Error in transcribing audio";
        }
    }

    // ChatGPT API를 호출해 AI 응답을 가져옴
    public String fetchAIResponse(String prompt) {
        String url = "https://api.openai.com/v1/chat/completions";

        // OpenAI ChatGPT API 호출 및 응답 처리 로직
        try (CloseableHttpClient client = HttpClients.createDefault()) {
            HttpPost request = new HttpPost(url);
            request.setHeader("Authorization", "Bearer " + apiKey);
            request.setHeader("Content-Type", "application/json");

            StringEntity requestEntity = new StringEntity(
                    // prompt를 포함한 요청을 JSON 형식으로 전송
                    // ChatGPT API 호출
                    "{\"model\": \"gpt-3.5-turbo\", \"messages\": [{\"role\": \"user\", \"content\": \"" + prompt + "\"}]}");
            request.setEntity(requestEntity);

            String responseString = EntityUtils.toString(client.execute(request).getEntity());
            JsonNode responseJson = objectMapper.readTree(responseString);

            // ChatGPT API에서 반환한 JSON 응답에서 "choices" 배열의 첫 번째 항목에서 "message"의 "content"를 추출하여 반환
            return responseJson.get("choices").get(0).get("message").get("content").asText();
        }
        catch (Exception e) {
            e.printStackTrace();
            return "Error in fetching AI response";
        }
    }

    // 텍스트를 한국어 음성 데이터로 변환
    public byte[] synthesizeAudioFromText(String text) {
        String url = "https://api.openai.com/v1/audio/generate";

        // OpenAI TTS API 호출 및 응답 처리 로직
        try (CloseableHttpClient client = HttpClients.createDefault()) {
            HttpPost request = new HttpPost(url);
            request.setHeader("Authorization", "Bearer " + apiKey);
            request.setHeader("Content-Type", "application/json");

            StringEntity requestEntity = new StringEntity(
                    // text를 JSON 형식의 요청 본문에 포함해 OpenAI의 TTS API로 전송
                    "{\"model\": \"text-to-speech-1\", \"text\": \"" + text + "\", \"voice\": \"alloy\", \"language\": \"ko\"}");
            request.setEntity(requestEntity);


//            오디오 파일을 byte[]로 받아 반환
//            byte[] responseBytes = EntityUtils.toByteArray(client.execute(request).getEntity());
//            return responseBytes;
            return EntityUtils.toByteArray(client.execute(request).getEntity());
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

}
