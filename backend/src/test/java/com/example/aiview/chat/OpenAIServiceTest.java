package com.example.aiview.chat;

import com.example.aiview.chat.service.OpenAIService;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.*;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@SpringBootTest
public class OpenAIServiceTest {

    @InjectMocks
    private OpenAIService openAIService;

    @Mock
    private CloseableHttpClient httpClient;

    @Mock
    private CloseableHttpResponse response;

    private final ObjectMapper objectMapper = new ObjectMapper();

    @BeforeEach
    public void setup() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testTranscribeAudioToText() throws Exception {
        // Mock API 응답 생성
        String mockResponse = "{\"text\": \"Hello, this is a test transcription\"}";
        when(response.getEntity()).thenReturn(new StringEntity(mockResponse));
        when(httpClient.execute(any(HttpPost.class))).thenReturn(response);

        byte[] audioData = "dummy-audio".getBytes();
        String result = openAIService.transcribeAudioToText(audioData);

        assertEquals("Hello, this is a test transcription", result);
    }

    @Test
    public void testFetchAIResponse() throws Exception {
        // Mock API 응답 생성
        String mockResponse = "{\"choices\": [{\"message\": {\"content\": \"This is a test response from AI\"}}]}";
        when(response.getEntity()).thenReturn(new StringEntity(mockResponse));
        when(httpClient.execute(any(HttpPost.class))).thenReturn(response);

        String prompt = "Test prompt";
        String result = openAIService.fetchAIResponse(prompt);

        assertEquals("This is a test response from AI", result);
    }

    @Test
    public void testSynthesizeAudioFromText() throws Exception {
        // Mock API 응답 생성 (바이트 배열)
        byte[] mockAudioData = "dummy-audio-data".getBytes();
        when(response.getEntity()).thenReturn(new ByteArrayEntity(mockAudioData));
        when(httpClient.execute(any(HttpPost.class))).thenReturn(response);

        String text = "Test text to synthesize";
        byte[] result = openAIService.synthesizeAudioFromText(text);

        assertArrayEquals(mockAudioData, result);
    }

}
