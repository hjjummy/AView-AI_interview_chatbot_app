package com.example.aiview.User;

import com.example.aiview.FirebaseTokenVerifier;
import com.google.firebase.auth.FirebaseToken;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;

@RestController
@RequestMapping("/api/user")
public class UserController {

    // private final UserRepository userRepository = new UserRepositoryImpl();

    private final UserRepository userRepository;

    public UserController(UserRepositoryImpl userRepository) {
        this.userRepository = userRepository;
    }

    @PostMapping("/save")
    public ResponseEntity<String> saveUser(@RequestHeader("Authorization") String idToken, @RequestBody User user) {
        FirebaseToken decodedToken = FirebaseTokenVerifier.verifyToken(idToken.replace("Bearer ", ""));
        if (decodedToken != null) {
            String uid = decodedToken.getUid();
            user.setIdUser(Long.valueOf(uid)); // Firebase UID를 User ID로 설정하여 고유 사용자 식별

            userRepository.save(user);
            return ResponseEntity.ok("User registered successfully.");
        } else {
            return ResponseEntity.status(401).body("Invalid Firebase token.");
        }
    }
}
