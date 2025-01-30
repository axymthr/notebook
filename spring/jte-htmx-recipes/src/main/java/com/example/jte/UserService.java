// File: UserService.java
package com.example.jte;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class UserService {

    @Autowired
    private UsersConfig usersConfig;

    public List<User> getAllUsers() {
        // Return all users sorted by name
        return usersConfig.getResults().stream()
                .sorted((a, b) -> a.name().first().compareToIgnoreCase(b.name().first()))
                .collect(Collectors.toList());
    }

    public List<User> searchUsers(String query) {
        if (query == null || query.isEmpty()) {
            return List.of();
        }
        String lowerCaseQuery = query.toLowerCase();
        return getAllUsers().stream()
                .filter(user -> user.name().first().toLowerCase().contains(lowerCaseQuery))
                .collect(Collectors.toList());
    }
}