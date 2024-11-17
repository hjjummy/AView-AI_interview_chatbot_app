package com.example.aiview.User;


public class User {
    private Long idUser;
    private String email;
    private String name;
    private int age;
    private Gender gender;
    private Role role;

    public User(Long idUser, String email, String name, int age, Gender gender, Role role) {
        this.idUser = idUser;
        this.email = email;
        this.name = name;
        this.age = age;
        this.gender = gender;
        this.role = role;
    }

    public Long getIdUser() {
        return idUser;
    }

    public void setIdUser(Long idUser) {
        this.idUser = idUser;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public Gender getGender() {
        return gender;
    }

    public void setGender(Gender gender) {
        this.gender = gender;
    }

    public Role getRole() {
        return role;
    }

    public void setRole(Role role) {
        this.role = role;
    }
}
