package com.example.aiview.User;


import java.util.List;

public interface UserRepository {
    void save(User user);
    User findById(Long idUser);
    void delete(User user);
    List<User> findAll();
}