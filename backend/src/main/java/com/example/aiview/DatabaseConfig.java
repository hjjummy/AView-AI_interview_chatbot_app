package com.example.aiview;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConfig {

    // 데이터베이스 URL, 사용자 이름, 비밀번호 설정 => 사용자 이름, 비번 공백처리함
    private static final String DB_URL = "jdbc:mysql://localhost:3306/AiView"; // 실제 데이터베이스 정보로 변경
    private static final String DB_USERNAME = "";
    private static final String DB_PASSWORD = "";

    // 데이터베이스 연결을 반환하는 메서드
    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(DB_URL, DB_USERNAME, DB_PASSWORD);
    }
}
