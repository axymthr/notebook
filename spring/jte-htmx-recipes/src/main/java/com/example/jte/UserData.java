// File: User.java
package com.example.jte;

import java.util.List;

public record UserData(List<User> results) {}

record User(Name name, String email, Picture picture) {}

record Name(String first, String last) {}

record Picture(String large) {}